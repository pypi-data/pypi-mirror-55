#include "atm90e32.h"
#include "atm90e32_reg.h"
#include "esphome/core/log.h"

namespace esphome {
namespace atm90e32 {

static const char *TAG = "atm90e32";

void ATM90E32Component::update() {
  if (this->read16_(ATM90E32_REGISTER_METEREN) != 1) {
    this->status_set_warning();
    return;
  }

  if (this->phase_[0].voltage_sensor_ != nullptr) {
    this->phase_[0].voltage_sensor_->publish_state(this->get_line_voltage_a_());
  }
  if (this->phase_[1].voltage_sensor_ != nullptr) {
    this->phase_[1].voltage_sensor_->publish_state(this->get_line_voltage_b_());
  }
  if (this->phase_[2].voltage_sensor_ != nullptr) {
    this->phase_[2].voltage_sensor_->publish_state(this->get_line_voltage_c_());
  }
  if (this->phase_[0].current_sensor_ != nullptr) {
    this->phase_[0].current_sensor_->publish_state(this->get_line_current_a_());
  }
  if (this->phase_[1].current_sensor_ != nullptr) {
    this->phase_[1].current_sensor_->publish_state(this->get_line_current_b_());
  }
  if (this->phase_[2].current_sensor_ != nullptr) {
    this->phase_[2].current_sensor_->publish_state(this->get_line_current_c_());
  }
  if (this->phase_[0].power_sensor_ != nullptr) {
    this->phase_[0].power_sensor_->publish_state(this->get_active_power_a_());
  }
  if (this->phase_[1].power_sensor_ != nullptr) {
    this->phase_[1].power_sensor_->publish_state(this->get_active_power_b_());
  }
  if (this->phase_[2].power_sensor_ != nullptr) {
    this->phase_[2].power_sensor_->publish_state(this->get_active_power_c_());
  }
  if (this->freq_sensor_ != nullptr) {
    this->freq_sensor_->publish_state(this->get_frequency_());
  }
  this->status_clear_warning();
}

void ATM90E32Component::setup() {
  ESP_LOGCONFIG(TAG, "Setting up ATM90E32Component...");
  this->spi_setup();

  uint16_t mmode0 = 0x185;
  if (line_freq_ == 60) {
    mmode0 |= 1 << 12;
  }

  this->write16_(ATM90E32_REGISTER_SOFTRESET, 0x789A);    // Perform soft reset
  this->write16_(ATM90E32_REGISTER_CFGREGACCEN, 0x55AA);  // enable register config access
  this->write16_(ATM90E32_REGISTER_METEREN, 0x0001);      // Enable Metering
  if (this->read16_(ATM90E32_REGISTER_LASTSPIDATA) != 0x0001) {
    ESP_LOGW(TAG, "Could not initialize ATM90E32 IC, check SPI settings");
    this->mark_failed();
    return;
  }

  this->write16_(ATM90E32_REGISTER_ZXCONFIG, 0x0A55);                    // ZX2, ZX1, ZX0 pin config
  this->write16_(ATM90E32_REGISTER_MMODE0, mmode0);                      // Mode Config (frequency set in main program)
  this->write16_(ATM90E32_REGISTER_MMODE1, pga_gain_);                   // PGA Gain Configuration for Current Channels
  this->write16_(ATM90E32_REGISTER_PSTARTTH, 0x0AFC);                    // Active Startup Power Threshold = 50%
  this->write16_(ATM90E32_REGISTER_QSTARTTH, 0x0AEC);                    // Reactive Startup Power Threshold = 50%
  this->write16_(ATM90E32_REGISTER_PPHASETH, 0x00BC);                    // Active Phase Threshold = 10%
  this->write16_(ATM90E32_REGISTER_UGAINA, this->phase_[0].volt_gain_);  // A Voltage rms gain
  this->write16_(ATM90E32_REGISTER_IGAINA, this->phase_[0].ct_gain_);    // A line current gain
  this->write16_(ATM90E32_REGISTER_UGAINB, this->phase_[1].volt_gain_);  // B Voltage rms gain
  this->write16_(ATM90E32_REGISTER_IGAINB, this->phase_[1].ct_gain_);    // B line current gain
  this->write16_(ATM90E32_REGISTER_UGAINC, this->phase_[2].volt_gain_);  // C Voltage rms gain
  this->write16_(ATM90E32_REGISTER_IGAINC, this->phase_[2].ct_gain_);    // C line current gain
  this->write16_(ATM90E32_REGISTER_CFGREGACCEN, 0x0000);                 // end configuration
}

void ATM90E32Component::dump_config() {
  ESP_LOGCONFIG("", "ATM90E32:");
  LOG_PIN("  CS Pin: ", this->cs_);
  if (this->is_failed()) {
    ESP_LOGE(TAG, "Communication with ATM90E32 failed!");
  }
  LOG_UPDATE_INTERVAL(this);
  LOG_SENSOR("  ", "Voltage A", this->phase_[0].voltage_sensor_);
  LOG_SENSOR("  ", "Current A", this->phase_[0].current_sensor_);
  LOG_SENSOR("  ", "Power A", this->phase_[0].power_sensor_);
  LOG_SENSOR("  ", "Voltage B", this->phase_[1].voltage_sensor_);
  LOG_SENSOR("  ", "Current B", this->phase_[1].current_sensor_);
  LOG_SENSOR("  ", "Power B", this->phase_[1].power_sensor_);
  LOG_SENSOR("  ", "Voltage C", this->phase_[2].voltage_sensor_);
  LOG_SENSOR("  ", "Current C", this->phase_[2].current_sensor_);
  LOG_SENSOR("  ", "Power C", this->phase_[2].power_sensor_);
  LOG_SENSOR("  ", "Frequency", this->freq_sensor_)
}
float ATM90E32Component::get_setup_priority() const { return setup_priority::DATA; }

uint16_t ATM90E32Component::read16_(uint16_t a_register) {
  uint8_t addrh = (1 << 7) | ((a_register >> 8) & 0x03);
  uint8_t addrl = (a_register & 0xFF);
  uint8_t data[2];
  uint16_t output;

  this->enable();
  delayMicroseconds(10);
  this->write_byte(addrh);
  this->write_byte(addrl);
  delayMicroseconds(4);
  this->read_array(data, 2);
  this->disable();

  output = (uint16_t(data[0] & 0xFF) << 8) | (data[1] & 0xFF);
  ESP_LOGVV(TAG, "read16_ 0x%04X output 0x%04X", a_register, output);
  return output;
}

int ATM90E32Component::read32_(uint16_t addr_h, uint16_t addr_l) {
  uint16_t val_h = this->read16_(addr_h);
  uint16_t val_l = this->read16_(addr_l);
  int32_t val = (val_h << 16) | val_l;

  ESP_LOGVV(TAG, "read32_ addr_h 0x%04X val_h 0x%04X addr_l 0x%04X val_l 0x%04X = %d", addr_h, val_h, addr_l, val_l,
            val);

  return val;
}

void ATM90E32Component::write16_(uint16_t a_register, uint16_t val) {
  uint8_t addrh = (a_register >> 8) & 0x03;
  uint8_t addrl = (a_register & 0xFF);

  ESP_LOGVV(TAG, "write16_ 0x%04X val 0x%04X", a_register, val);
  this->enable();
  delayMicroseconds(10);
  this->write_byte(addrh);
  this->write_byte(addrl);
  delayMicroseconds(4);
  this->write_byte((val >> 8) & 0xff);
  this->write_byte(val & 0xFF);
  this->disable();
}

float ATM90E32Component::get_line_voltage_a_() {
  uint16_t voltage = this->read16_(ATM90E32_REGISTER_URMSA);
  return (float) voltage / 100;
}
float ATM90E32Component::get_line_voltage_b_() {
  uint16_t voltage = this->read16_(ATM90E32_REGISTER_URMSB);
  return (float) voltage / 100;
}
float ATM90E32Component::get_line_voltage_c_() {
  uint16_t voltage = this->read16_(ATM90E32_REGISTER_URMSC);
  return (float) voltage / 100;
}
float ATM90E32Component::get_line_current_a_() {
  uint16_t current = this->read16_(ATM90E32_REGISTER_IRMSA);
  return (float) current / 1000;
}
float ATM90E32Component::get_line_current_b_() {
  uint16_t current = this->read16_(ATM90E32_REGISTER_IRMSB);
  return (float) current / 1000;
}
float ATM90E32Component::get_line_current_c_() {
  uint16_t current = this->read16_(ATM90E32_REGISTER_IRMSC);
  return (float) current / 1000;
}
float ATM90E32Component::get_active_power_a_() {
  int val = this->read32_(ATM90E32_REGISTER_PMEANA, ATM90E32_REGISTER_PMEANALSB);
  return val * 0.00032f;
}
float ATM90E32Component::get_active_power_b_() {
  int val = this->read32_(ATM90E32_REGISTER_PMEANB, ATM90E32_REGISTER_PMEANBLSB);
  return val * 0.00032f;
}
float ATM90E32Component::get_active_power_c_() {
  int val = this->read32_(ATM90E32_REGISTER_PMEANC, ATM90E32_REGISTER_PMEANCLSB);
  return val * 0.00032f;
}
float ATM90E32Component::get_frequency_() {
  uint16_t freq = this->read16_(ATM90E32_REGISTER_FREQ);
  return (float) freq / 100;
}
}  // namespace atm90e32
}  // namespace esphome
