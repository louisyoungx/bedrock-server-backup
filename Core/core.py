import time
from threading import Thread
from Config.settings import config
from Archive.manager import monthlyManager, dailyManager, minutelyManager
def main():
    
    DEBUG = config.settings("Debug", "DEBUG")
    
    if not DEBUG:
        # running with thread，add time sleep to prevent instantaneous I/O overload
        thread_monthly = Thread(target=monthlyManager.running)
        thread_daily = Thread(target=dailyManager.running)
        thread_minutely = Thread(target=minutelyManager.running)

        thread_monthly.start()
        time.sleep(10)
        thread_daily.start()
        time.sleep(10)
        thread_minutely.start()
        
    else:
        # testing code
        thread_minutely = Thread(target=minutelyManager.running)
        thread_minutely.start()
        time.sleep(10)
        minutelyManager.load()
        for i in minutelyManager.list():
            print(i.filename)
