
# standard
import datetime


def now():
    return int(datetime.datetime.now().strftime("%s"))


def load(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)
