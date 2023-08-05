from __future__ import print_function

import collections
import io
import logging
import os
import re
import subprocess
import sys

from esphome import const
from esphome.py_compat import IS_PY2, decode_text, text_type

_LOGGER = logging.getLogger(__name__)


class RegistryEntry(object):
    def __init__(self, name, fun, type_id, schema):
        self.name = name
        self.fun = fun
        self.type_id = type_id
        self.raw_schema = schema

    @property
    def coroutine_fun(self):
        from esphome.core import coroutine
        return coroutine(self.fun)

    @property
    def schema(self):
        from esphome.config_validation import Schema
        return Schema(self.raw_schema)


class Registry(dict):
    def __init__(self, base_schema=None, type_id_key=None):
        super(Registry, self).__init__()
        self.base_schema = base_schema or {}
        self.type_id_key = type_id_key

    def register(self, name, type_id, schema):
        def decorator(fun):
            self[name] = RegistryEntry(name, fun, type_id, schema)
            return fun

        return decorator


class SimpleRegistry(dict):
    def register(self, name, data):
        def decorator(fun):
            self[name] = (fun, data)
            return fun

        return decorator


def safe_print(message=""):
    from esphome.core import CORE

    if CORE.dashboard:
        try:
            message = message.replace('\033', '\\033')
        except UnicodeEncodeError:
            pass

    try:
        print(message)
        return
    except UnicodeEncodeError:
        pass

    try:
        print(message.encode('utf-8', 'backslashreplace'))
    except UnicodeEncodeError:
        try:
            print(message.encode('ascii', 'backslashreplace'))
        except UnicodeEncodeError:
            print("Cannot print line because of invalid locale!")


def shlex_quote(s):
    if not s:
        return u"''"
    if re.search(r'[^\w@%+=:,./-]', s) is None:
        return s

    return u"'" + s.replace(u"'", u"'\"'\"'") + u"'"


ANSI_ESCAPE = re.compile(r'\033[@-_][0-?]*[ -/]*[@-~]')


class RedirectText(object):
    def __init__(self, out, filter_lines=None):
        self._out = out
        if filter_lines is None:
            self._filter_pattern = None
        else:
            pattern = r'|'.join(r'(?:' + pattern + r')' for pattern in filter_lines)
            self._filter_pattern = re.compile(pattern)
        self._line_buffer = ''

    def __getattr__(self, item):
        return getattr(self._out, item)

    def _write_color_replace(self, s):
        from esphome.core import CORE

        if CORE.dashboard:
            # With the dashboard, we must create a little hack to make color output
            # work. The shell we create in the dashboard is not a tty, so python removes
            # all color codes from the resulting stream. We just convert them to something
            # we can easily recognize later here.
            s = s.replace('\033', '\\033')
        self._out.write(s)

    def write(self, s):
        # s is usually a text_type already (self._out is of type TextIOWrapper)
        # However, s is sometimes also a bytes object in python3. Let's make sure it's a
        # text_type
        # If the conversion fails, we will create an exception, which is okay because we won't
        # be able to print it anyway.
        text = decode_text(s)
        assert isinstance(text, text_type)

        if self._filter_pattern is not None:
            self._line_buffer += text
            lines = self._line_buffer.splitlines(True)
            for line in lines:
                if '\n' not in line and '\r' not in line:
                    # Not a complete line, set line buffer
                    self._line_buffer = line
                    break
                self._line_buffer = ''

                line_without_ansi = ANSI_ESCAPE.sub('', line)
                line_without_end = line_without_ansi.rstrip()
                if self._filter_pattern.match(line_without_end) is not None:
                    # Filter pattern matched, ignore the line
                    continue

                self._write_color_replace(line)
        else:
            self._write_color_replace(text)

        # write() returns the number of characters written
        # Let's print the number of characters of the original string in order to not confuse
        # any caller.
        return len(s)

    # pylint: disable=no-self-use
    def isatty(self):
        return True


def run_external_command(func, *cmd, **kwargs):
    def mock_exit(return_code):
        raise SystemExit(return_code)

    orig_argv = sys.argv
    orig_exit = sys.exit  # mock sys.exit
    full_cmd = u' '.join(shlex_quote(x) for x in cmd)
    _LOGGER.info(u"Running:  %s", full_cmd)

    filter_lines = kwargs.get('filter_lines')
    orig_stdout = sys.stdout
    sys.stdout = RedirectText(sys.stdout, filter_lines=filter_lines)
    orig_stderr = sys.stderr
    sys.stderr = RedirectText(sys.stderr, filter_lines=filter_lines)

    capture_stdout = kwargs.get('capture_stdout', False)
    if capture_stdout:
        cap_stdout = sys.stdout = io.StringIO()

    try:
        sys.argv = list(cmd)
        sys.exit = mock_exit
        return func() or 0
    except KeyboardInterrupt:
        return 1
    except SystemExit as err:
        return err.args[0]
    except Exception as err:  # pylint: disable=broad-except
        _LOGGER.error(u"Running command failed: %s", err)
        _LOGGER.error(u"Please try running %s locally.", full_cmd)
    finally:
        sys.argv = orig_argv
        sys.exit = orig_exit

        sys.stdout = orig_stdout
        sys.stderr = orig_stderr

        if capture_stdout:
            # pylint: disable=lost-exception
            return cap_stdout.getvalue()


def run_external_process(*cmd, **kwargs):
    full_cmd = u' '.join(shlex_quote(x) for x in cmd)
    _LOGGER.info(u"Running:  %s", full_cmd)
    filter_lines = kwargs.get('filter_lines')

    capture_stdout = kwargs.get('capture_stdout', False)
    if capture_stdout:
        sub_stdout = io.BytesIO()
    else:
        sub_stdout = RedirectText(sys.stdout, filter_lines=filter_lines)

    sub_stderr = RedirectText(sys.stderr, filter_lines=filter_lines)

    try:
        return subprocess.call(cmd,
                               stdout=sub_stdout,
                               stderr=sub_stderr)
    except Exception as err:  # pylint: disable=broad-except
        _LOGGER.error(u"Running command failed: %s", err)
        _LOGGER.error(u"Please try running %s locally.", full_cmd)
    finally:
        if capture_stdout:
            # pylint: disable=lost-exception
            return sub_stdout.getvalue()


def is_dev_esphome_version():
    return 'dev' in const.__version__


# Custom OrderedDict with nicer repr method for debugging
class OrderedDict(collections.OrderedDict):
    def __repr__(self):
        return dict(self).__repr__()

    def move_to_end(self, key, last=True):
        if IS_PY2:
            if len(self) == 1:
                return
            if last:
                # When moving to end, just pop and re-add
                val = self.pop(key)
                self[key] = val
            else:
                # When moving to front, use internals here
                # https://stackoverflow.com/a/16664932
                root = self._OrderedDict__root  # pylint: disable=no-member
                first = root[1]
                link = self._OrderedDict__map[key]  # pylint: disable=no-member
                link_prev, link_next, _ = link
                link_prev[1] = link_next
                link_next[0] = link_prev
                link[0] = root
                link[1] = first
                root[1] = first[0] = link
        else:
            super(OrderedDict, self).move_to_end(key, last=last)  # pylint: disable=no-member


def list_yaml_files(folder):
    files = filter_yaml_files([os.path.join(folder, p) for p in os.listdir(folder)])
    files.sort()
    return files


def filter_yaml_files(files):
    files = [f for f in files if os.path.splitext(f)[1] == '.yaml']
    files = [f for f in files if os.path.basename(f) != 'secrets.yaml']
    files = [f for f in files if not os.path.basename(f).startswith('.')]
    return files
