import copy

from Config.settings import config
from Archive.lock import forceLock, stopLock, monthlyLock, dailyLock, minutelyLock
from Archive.manager import monthlyManager, dailyManager, minutelyManager

def log(request):
    file_path = config.path() + config.settings("Logger", "FILE_PATH") + config.settings("Logger", "FILE_NAME")
    file_page_file = open(file_path, 'r')
    return str(file_page_file.read())

def serverConfig(request):
    appConfig = copy.deepcopy(config._config._sections)
    for model in appConfig:
        for item in appConfig[model]:
            appConfig[model][item] = eval(appConfig[model][item])
            value = appConfig[model][item]
            # DEBUG print(model, item, value, type(value))
    return appConfig

def lockStatus(request):
    data = [forceLock.status(), stopLock.status(), monthlyLock.status(), dailyLock.status(), minutelyLock.status()]
    return data

def lock(request):
    # accept: /lock?lockType=force/stop/monthly/daily/minutely
    lockType = request['lockType']
    eval(lockType + 'Lock').lock()
    return 'locked'
    
def unlock(request):
    # accept: /unlock?lockType=force/stop/monthly/daily/minutely
    lockType = request['lockType']
    eval(lockType + 'Lock').unlock()
    return 'unlocked'

def fallback(request):
    # accept: /fallback?archiveType=monthly/daily/minutely&index=1-9
    archiveType = request['archiveType']
    index = int(request['index'])
    eval(archiveType + 'Manager').fallback(index)
    return 'success'

def archiveList(request):
    # accept: /archive-list?archiveType=monthly/daily/minutely
    archiveType = request['archiveType']
    archiveList = eval(archiveType + 'Manager').list()
    return archiveList