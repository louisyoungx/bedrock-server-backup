import os
from Config.settings import config
from Logger.logger import logger
from Archive.archive import monthlyArchive, dailyArchive, minutelyArchive

def run(command):
    DEBUG = config.settings("Debug", "DEBUG")
    if DEBUG:
        logger.info(command)
    os.system(command)

class ArchiveHandler(object):
    archive = None
    mode = config.settings("Archive", "MODE")  # Docker / Local
    dockerID = config.settings("Archive", "DOCKER_ID")
    archiveFilePath = config.settings("Archive", "ArchiveFilePath")
    archiveFileName = config.settings("Archive", "ArchiveFileName")

    def __init__(self, archive):
        self.archive = archive
        if self.mode == 'Docker' and self.dockerID != '':
            logger.info('ArchiveHandler Mode : Docker')
        elif self.mode == 'Local':
            logger.info('ArchiveHandler Mode : Docker')
        else:
            raise Exception('mode field wrong or dockerID is null')

    def read(self):
        """ copy archive file """
        filename = self.archive.filename()
        if self.mode == 'Docker':
            self._docker_read()
        elif self.mode == 'Local':
            self._local_read()
        self.zip(filename)
        self.move_to_storage(filename)
        return filename + '.zip'

    def write(self, filename):
        """ write archive file """
        self.copy_to_buffer(filename)
        self.unzip(filename)
        if self.mode == 'Docker':
            self._docker_write()
        elif self.mode == 'Local':
            self._local_write()

    def delete(self, filename):
        """ delete archive file from storage """
        run(f'rm {self.archive.storage}/{filename}')

    def _local_read(self):
        """ copy archive file directory and save to buffer """
        run(f'cp -r {self.archiveFilePath}/{self.archiveFileName} {self.archive.buffer}')

    def _local_write(self):
        """ write archive file directory from buffer """
        run(f'cp -r {self.archive.buffer}/{self.archiveFileName} {self.archiveFilePath}/')
        run(f'rm -rf {self.archive.buffer}/{self.archiveFileName}')

    def _docker_read(self):
        """ copy archive file directory from docker and save to buffer """
        run(f'docker cp {self.dockerID}:{self.archiveFilePath}/{self.archiveFileName} {self.archive.buffer}')

    def _docker_write(self):
        """ write archive file directory to docker from buffer """
        run(f'docker cp {self.archive.buffer}/{self.archiveFileName} {self.dockerID}:{self.archiveFilePath}/')
        run(f'rm -rf {self.archive.buffer}/{self.archiveFileName}')
        run(f'docker restart {self.dockerID}')

    def zip(self, filename):
        """ zip archive file """
        os.chdir(self.archive.buffer)
        run(f'zip -m -r {filename}.zip {self.archiveFileName}')

    def unzip(self, filename):
        """ zip archive file """
        run(f'unzip -o -d {self.archive.buffer} {self.archive.buffer}/{filename}')
        run(f'rm {self.archive.buffer}/{filename}')

    def copy_to_buffer(self, filename):
        """ move file to buffer from storage """
        run(f'cp {self.archive.storage}/{filename} {self.archive.buffer} ')

    def move_to_storage(self, filename):
        """ move file to storage from buffer """
        run(f'mv {self.archive.buffer}/{filename}.zip {self.archive.storage}')


monthlyHandler = ArchiveHandler(monthlyArchive)
dailyHandler = ArchiveHandler(dailyArchive)
minutelyHandler = ArchiveHandler(minutelyArchive)
