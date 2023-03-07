from datetime import datetime


def get_current_partition():
    return datetime.utcnow().strftime("%Y-%m-%d")
