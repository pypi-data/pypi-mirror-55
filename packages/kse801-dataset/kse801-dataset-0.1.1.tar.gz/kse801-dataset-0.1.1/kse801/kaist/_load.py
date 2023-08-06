from kse801._util import _load_data


def load_accel():
    return _load_data('kaist', 'accelerometer')


def load_activity():
    return _load_data('kaist', 'activity_event')


def load_app_usage():
    return _load_data('kaist', 'app_usage')


def load_data_traffic():
    return _load_data('kaist', 'data_traffic')


def load_gsr():
    return _load_data('kaist', 'gsr')


def load_heartrate():
    return _load_data('kaist', 'heart_rate')


def load_location():
    return _load_data('kaist', 'location')


def load_rr_interval():
    return _load_data('kaist', 'rr_interval')


def load_skin_temperature():
    return _load_data('kaist', 'skin_temperature')

