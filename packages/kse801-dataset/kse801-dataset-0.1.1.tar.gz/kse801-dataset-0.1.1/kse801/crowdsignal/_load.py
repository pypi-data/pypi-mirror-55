from kse801._util import _load_data


def load_accel_phone():
    return _load_data('crowdsignal', 'accelerometer_phone')


def load_accel_watch():
    return _load_data('crowdsignal', 'accelerometer_smartwatch')


def load_battery_phone():
    return _load_data('crowdsignal', 'battery_phone')


def load_battery_watch():
    return _load_data('crowdsignal', 'battery_smartwatch')


def load_bluetooth_phone():
    return _load_data('crowdsignal', 'bluetooth_phone')


def load_connectivity_phone():
    return _load_data('crowdsignal', 'connectivity_phone')


def load_gsm_phone():
    return _load_data('crowdsignal', 'gsm_phone')


def load_gyro_phone():
    return _load_data('crowdsignal', 'gyroscope_phone')


def load_gyro_watch():
    return _load_data('crowdsignal', 'gyroscope_smartwatch')


def load_heartrate_watch():
    return _load_data('crowdsignal', 'heart_rate_smartwatch')


def load_label():
    return _load_data('crowdsignal', 'labels')


def load_light_phone():
    return _load_data('crowdsignal', 'light_phone')


def load_location_phone():
    return _load_data('crowdsignal', 'location_phone')


def load_magnet_phone():
    return _load_data('crowdsignal', 'magnetometer_phone')


def load_magnet_watch():
    return _load_data('crowdsignal', 'magnetometer_smartwatch')


def load_pressure_phone():
    return _load_data('crowdsignal', 'pressure_phone')


def load_proximity_phone():
    return _load_data('crowdsignal', 'proximity_phone')


def load_screen_phone():
    return _load_data('crowdsignal', 'screen_phone')


def load_sms_phone():
    return _load_data('crowdsignal', 'sms_phone')


def load_wlan_phone():
    return _load_data('crowdsignal', 'wlan_phone')
