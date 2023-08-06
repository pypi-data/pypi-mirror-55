from kse801._util import _load_data


def load_activity():
    return _load_data('abc', 'activity')


def load_app_usage():
    return _load_data('abc', 'app_usage')


def load_plugged():
    return _load_data('abc', 'plugged')


def load_ringer_mode():
    return _load_data('abc', 'ringer_mode')


def load_screen():
    return _load_data('abc', 'screen')


def load_location():
    return _load_data('abc', 'location')


def load_receptivity():
    return _load_data('abc', 'receptivity')
