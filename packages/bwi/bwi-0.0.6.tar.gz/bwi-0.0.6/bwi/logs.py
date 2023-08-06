import os
from datetime import datetime
import _queue_sender


def _generate_message(level: str, message: str):
    _queue_sender.send_to_queue("logs", {'level': level, 'message': message,
                                         'timestamp': datetime.timestamp(
                                             datetime.now())})
    return "Message sended"


def debug(message: str):
    """
    Log a message with debug level

    :param message: the message to log
    """
    if os.environ.get('BWI_INFRA') is not None:
        _generate_message("debug", message)
    else:
        print(message)


def info(message: str):
    """
    Log a message with info level

    :param message: the message to log
    """
    if os.environ.get('BWI_INFRA') is not None:
        _generate_message("info", message)
    else:
        print(message)


def warning(message: str):
    """
    Log a message with warning level

    :param message: the message to log
    """
    if os.environ.get('BWI_INFRA') is not None:
        _generate_message("warning", message)
    else:
        print(message)


def error(message: str):
    """
    Log a message with error level

    :param message: the message to log
    """
    if os.environ.get('BWI_INFRA') is not None:
        _generate_message("error", message)
    else:
        print(message)


def critical(message: str):
    """
    Log a message with critical level

    :param message: the message to log
    """
    if os.environ.get('BWI_INFRA') is not None:
        _generate_message("critical", message)
    else:
        print(message)


if __name__ == '__main__':
    debug("test")
    info("test")
    warning("test")
    error("test")
    os.environ['BWI_INFRA'] = "trou"
    debug("test")
    info("test")
    warning("test")
    error("test")
