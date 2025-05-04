from datetime import datetime


def get_time_now() -> int:
    return int(datetime.now().timestamp())
