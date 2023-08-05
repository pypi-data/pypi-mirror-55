#include "api_server.h"
#include "api_connection.h"
#include "esphome/core/log.h"
#include "esphome/core/application.h"
#include "esphome/core/util.h"
#include "esphome/core/defines.h"
#include "esphome/core/version.h"

#ifdef USE_LOGGER
#include "esphome/components/logger/logger.h"
#endif

#include <algorithm>

namespace esphome {
namespace api {

static const char *TAG = "api";

// APIServer
void APIServer::setup() {
  ESP_LOGCONFIG(TAG, "Setting up Home Assistant API server...");
  this->setup_controller();
  this->server_ = AsyncServer(this->port_);
  this->server_.setNoDelay(false);
  this->server_.begin();
  this->server_.onClient(
      [](void *s, AsyncClient *client) {
        if (client == nullptr)
          return;

        // can't print here because in lwIP thread
        // ESP_LOGD(TAG, "New client connected from %s", client->remoteIP().toString().c_str());
        auto *a_this = (APIServer *) s;
        a_this->clients_.push_back(new APIConnection(client, a_this));
      },
      this);
#ifdef USE_LOGGER
  if (logger::global_logger != nullptr) {
    logger::global_logger->add_on_log_callback([this](int level, const char *tag, const char *message) {
      for (auto *c : this->clients_) {
        if (!c->remove_)
          c->send_log_message(level, tag, message);
      }
    });
  }
#endif

  this->last_connected_ = millis();

#ifdef USE_ESP32_CAMERA
  if (esp32_camera::global_esp32_camera != nullptr) {
    esp32_camera::global_esp32_camera->add_image_callback([this](std::shared_ptr<esp32_camera::CameraImage> image) {
      for (auto *c : this->clients_)
        if (!c->remove_)
          c->send_camera_state(image);
    });
  }
#endif
}
void APIServer::loop() {
  // Partition clients into remove and active
  auto new_end =
      std::partition(this->clients_.begin(), this->clients_.end(), [](APIConnection *conn) { return !conn->remove_; });
  // print disconnection messages
  for (auto it = new_end; it != this->clients_.end(); ++it) {
    ESP_LOGD(TAG, "Disconnecting %s", (*it)->client_info_.c_str());
  }
  // only then delete the pointers, otherwise log routine
  // would access freed memory
  for (auto it = new_end; it != this->clients_.end(); ++it)
    delete *it;
  // resize vector
  this->clients_.erase(new_end, this->clients_.end());

  for (auto *client : this->clients_) {
    client->loop();
  }

  if (this->reboot_timeout_ != 0) {
    const uint32_t now = millis();
    if (!this->is_connected()) {
      if (now - this->last_connected_ > this->reboot_timeout_) {
        ESP_LOGE(TAG, "No client connected to API. Rebooting...");
        App.reboot();
      }
      this->status_set_warning();
    } else {
      this->last_connected_ = now;
      this->status_clear_warning();
    }
  }
}
void APIServer::dump_config() {
  ESP_LOGCONFIG(TAG, "API Server:");
  ESP_LOGCONFIG(TAG, "  Address: %s:%u", network_get_address().c_str(), this->port_);
}
bool APIServer::uses_password() const { return !this->password_.empty(); }
bool APIServer::check_password(const std::string &password) const {
  // depend only on input password length
  const char *a = this->password_.c_str();
  uint32_t len_a = this->password_.length();
  const char *b = password.c_str();
  uint32_t len_b = password.length();

  // disable optimization with volatile
  volatile uint32_t length = len_b;
  volatile const char *left = nullptr;
  volatile const char *right = b;
  uint8_t result = 0;

  if (len_a == length) {
    left = *((volatile const char **) &a);
    result = 0;
  }
  if (len_a != length) {
    left = b;
    result = 1;
  }

  for (size_t i = 0; i < length; i++) {
    result |= *left++ ^ *right++;  // NOLINT
  }

  return result == 0;
}
void APIServer::handle_disconnect(APIConnection *conn) {}
#ifdef USE_BINARY_SENSOR
void APIServer::on_binary_sensor_update(binary_sensor::BinarySensor *obj, bool state) {
  if (obj->is_internal())
    return;
  for (auto *c : this->clients_)
    c->send_binary_sensor_state(obj, state);
}
#endif

#ifdef USE_COVER
void APIServer::on_cover_update(cover::Cover *obj) {
  if (obj->is_internal())
    return;
  for (auto *c : this->clients_)
    c->send_cover_state(obj);
}
#endif

#ifdef USE_FAN
void APIServer::on_fan_update(fan::FanState *obj) {
  if (obj->is_internal())
    return;
  for (auto *c : this->clients_)
    c->send_fan_state(obj);
}
#endif

#ifdef USE_LIGHT
void APIServer::on_light_update(light::LightState *obj) {
  if (obj->is_internal())
    return;
  for (auto *c : this->clients_)
    c->send_light_state(obj);
}
#endif

#ifdef USE_SENSOR
void APIServer::on_sensor_update(sensor::Sensor *obj, float state) {
  if (obj->is_internal())
    return;
  for (auto *c : this->clients_)
    c->send_sensor_state(obj, state);
}
#endif

#ifdef USE_SWITCH
void APIServer::on_switch_update(switch_::Switch *obj, bool state) {
  if (obj->is_internal())
    return;
  for (auto *c : this->clients_)
    c->send_switch_state(obj, state);
}
#endif

#ifdef USE_TEXT_SENSOR
void APIServer::on_text_sensor_update(text_sensor::TextSensor *obj, std::string state) {
  if (obj->is_internal())
    return;
  for (auto *c : this->clients_)
    c->send_text_sensor_state(obj, state);
}
#endif

#ifdef USE_CLIMATE
void APIServer::on_climate_update(climate::Climate *obj) {
  if (obj->is_internal())
    return;
  for (auto *c : this->clients_)
    c->send_climate_state(obj);
}
#endif

float APIServer::get_setup_priority() const { return setup_priority::AFTER_WIFI; }
void APIServer::set_port(uint16_t port) { this->port_ = port; }
APIServer *global_api_server = nullptr;

void APIServer::set_password(const std::string &password) { this->password_ = password; }
void APIServer::send_homeassistant_service_call(const HomeassistantServiceResponse &call) {
  for (auto *client : this->clients_) {
    client->send_homeassistant_service_call(call);
  }
}
APIServer::APIServer() { global_api_server = this; }
void APIServer::subscribe_home_assistant_state(std::string entity_id, std::function<void(std::string)> f) {
  this->state_subs_.push_back(HomeAssistantStateSubscription{
      .entity_id = std::move(entity_id),
      .callback = std::move(f),
  });
}
const std::vector<APIServer::HomeAssistantStateSubscription> &APIServer::get_state_subs() const {
  return this->state_subs_;
}
uint16_t APIServer::get_port() const { return this->port_; }
void APIServer::set_reboot_timeout(uint32_t reboot_timeout) { this->reboot_timeout_ = reboot_timeout; }
#ifdef USE_HOMEASSISTANT_TIME
void APIServer::request_time() {
  for (auto *client : this->clients_) {
    if (!client->remove_ && client->connection_state_ == APIConnection::ConnectionState::CONNECTED)
      client->send_time_request();
  }
}
#endif
bool APIServer::is_connected() const { return !this->clients_.empty(); }
void APIServer::on_shutdown() {
  for (auto *c : this->clients_) {
    c->send_disconnect_request(DisconnectRequest());
  }
  delay(10);
}

}  // namespace api
}  // namespace esphome
