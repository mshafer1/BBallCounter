__author__ = 'Matthew'
import datetime

def timeStamp():
    return "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())

if __name__ == '__main__':
    print timeStamp()