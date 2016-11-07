__author__ = 'Matthew'
import datetime


def time_stamp():
    return "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())

if __name__ == '__main__':
    print time_stamp()