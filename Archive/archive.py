import time
import calendar
import datetime
from Config.settings import config
from Logger.logger import logger
from Archive.lock import monthlyLock, dailyLock, minutelyLock


class Archive(object):
    type = None  # Monthly / Daily / Minutely
    interval = None  # backup interval
    capacity = 10   # capacity of archive can be backup
    # time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    fileFormat = '%Y-%m-%d %H:%M:%S'
    lock = None

    def __init__(self):
        if self.type == None:
            raise Exception('archive type is not defined')
        self.buffer = config.path() + '/Buffer/' + self.type  # the buffer file path
        self.storage = config.path() + '/Storage/' + self.type  # the storage file path
        logger.info(self.type + ' Archive Initialized')

    def status(self):
        return {
            'Type': self.Type,
            'buffer': self.buffer,
            'storage': self.storage,
            'interval': self.interval,
        }

    def filename(self):
        return time.strftime(self.fileFormat, time.localtime())


def MonthDays():
    now = datetime.datetime.now()
    days = calendar.monthrange(now.year, now.month)[1]
    return days


class MonthlyArchive(Archive):
    type = 'Monthly'
    interval = 60 * 60 * 24 * MonthDays()
    fileFormat = '%Y-%m'
    lock = monthlyLock


class DailyArchive(Archive):
    type = 'Daily'
    interval = 60 * 60 * 24
    fileFormat = '%m-%d'
    lock = dailyLock


class MinutelyArchive(Archive):
    type = 'Minutely'
    interval = 60 * 5
    capacity = 6
    fileFormat = '%H:%M'
    lock = minutelyLock


monthlyArchive = MonthlyArchive()
dailyArchive = DailyArchive()
minutelyArchive = MinutelyArchive()
