from Server.api import *

def urls(url, request):
    if (url == "/log"): return log(request)
    elif (url == "/system-info"): return systemInfo(request)
    elif (url == "/config"): return serverConfig(request)
    elif (url == "/lock-status"): return lockStatus(request)
    elif (url == "/lock"): return lock(request)
    elif (url == "/unlock"): return unlock(request)
    elif (url == "/fallback"): return fallback(request)
    elif (url == "/archive-list"): return archiveList(request)
    else: return {'status': 'No Response', 'code': 404}