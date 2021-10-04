import time
from Logger.logger import logger

class Lock(object):
    lockStatus = False
    lockType = None
    lockTime = None

    def status(self):
        return {
            'status' : self.lockStatus,
            'type' : self.lockType,
            'time' : self.lockTime,
        }

    def lock(self):
        self.lockStatus = True
        self.lockTime = time.time()
        logger.info(self.lockType + 'Locked')
        return self.lockTime

    def unlock(self):
        self.lockStatus = False
        logger.info(self.lockType + 'UnLocked')
        return True

class ForceLock(Lock):
    """
    ForceLock
    when docker container or archive file donot exist, change lockType to 'force'
    """
    lockType = 'ForceLock'

class StopLock(Lock):
    """
    StopLock
    when user stop all archives
    """
    lockType = 'StopLock'

class MonthlyLock(Lock):
    lockType = 'MonthlyLock'

class DailyLock(Lock):
    lockType = 'DailyLock'

class MinutelyLock(Lock):
    lockType = 'MinutelyLock'

forceLock = ForceLock()
stopLock = StopLock()
monthlyLock = MonthlyLock()
dailyLock = DailyLock()
minutelyLock = MinutelyLock()

