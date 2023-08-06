import os
from datetime import datetime
import _queue_sender


def _generate_message(type: str, val: float, value: float):
    _queue_sender.send_to_queue("metrics", {'type': type, 'value': val,
                                            'timestamp': datetime.timestamp(
                                                datetime.now())})
    return "Message sended"


def inc(name: str, val: float):
    """
    Store an inc metric value
    :param name: the name of the metric
    :param val: the value of the current action
    """
    if os.environ.get('BWI_INFRA') is not None:
        _generate_message('inc', name, val)
    else:
        print(name, val)


def dec(name: str, val: float):
    """
    Store a dec metric value
    :param name: the name of the metric
    :param value: the value of the current action
    """
    if os.environ.get('BWI_INFRA') is not None:
        _generate_message('dec', name, val)
    else:
        print(name, val)


def value(name: str, val: float):
    """
    Store a numeric value
    :param name: the name of the metric
    :param value: the value of the current action
    """
    if os.environ.get('BWI_INFRA') is not None:
        _generate_message('value', name, val)
    else:
        print(name, val)


if __name__ == '__main__':
    inc("test", 1)
    dec("test", 1)
    value("test", 1)
    os.environ['BWI_INFRA'] = "trou"
    inc("test", 1)
    dec("test", 1)
    value("test", 1)
