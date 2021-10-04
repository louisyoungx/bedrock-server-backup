import time
import os
from Logger.logger import logger
from Archive.lock import forceLock, stopLock
from Archive.archive import monthlyArchive, dailyArchive, minutelyArchive
from Archive.handler import monthlyHandler, dailyHandler, minutelyHandler


class ArchiveFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.time = time.time()


class ArchiveManager(object):
    archive = None
    handler = None
    archiveList = None

    def __init__(self, archive, handler):
        self.archive = archive
        self.handler = handler
        self.archiveList = []
        for archiveName in os.listdir(self.archive.storage):
            if archiveName[0] == '.':
                continue
            self.archiveList.append(ArchiveFile(archiveName))

    def list(self):
        """ ArchiveFile object list """
        dictList = []
        for obj in self.archiveList:
            dictList.append({
                'filename': obj.filename,
                'time': time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(obj.time))
            })
        return dictList

    def running(self):
        """ backup after interval time """
        while True:

            if forceLock.lockStatus:
                logger.error(
                    'ForceLock: docker container or archive file donot exist')

            elif stopLock.lockStatus:
                logger.warning('StopLock: user stopped all archives')

            elif self.archive.lock.lockStatus:
                logger.warning(self.archive.lock.lockType +
                               f': user stopped {self.archive.type} archives')

            else:
                if len(self.archiveList) >= self.archive.capacity:
                    deleteFile = self.archiveList.pop()
                    self.handler.delete(deleteFile.filename)
                filename = self.save()
                newFile = ArchiveFile(filename)
                self.archiveList.insert(0, newFile)

            logger.info(f'waiting for start after {self.archive.interval} s')
            time.sleep(self.archive.interval)

    def save(self):
        """ save archive file """
        filename = self.handler.read()
        logger.info(f'save archive {filename} successfully')
        return filename

    def load(self):
        """ load latest archive file """
        self.fallback(0)

    def fallback(self, index):
        """ fallback No.index archive file """
        filename = self.archiveList[index].filename
        self.handler.write(filename)
        logger.info(f'load archive {filename} successfully')


monthlyManager = ArchiveManager(monthlyArchive, monthlyHandler)
dailyManager = ArchiveManager(dailyArchive, dailyHandler)
minutelyManager = ArchiveManager(minutelyArchive, minutelyHandler)
