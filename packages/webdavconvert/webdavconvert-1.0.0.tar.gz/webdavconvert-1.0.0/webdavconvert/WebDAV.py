import webdav3.client as wc
import os
import re
import logging
from .Util import *

logger = logging.getLogger(__name__)

class CloudConnection:
    """Base class wrapping the webdav3 client."""
    URL = False
    USER = False
    PASSWORD = False
    ROOT = '/'

    def __init__(self, url=False, username=False, password=False, root=False):
        self.url = url or CloudConnection.URL
        self.username = username or CloudConnection.USER
        self.password = password or CloudConnection.PASSWORD
        self.root = root or CloudConnection.ROOT
        self.connect()

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, value: str):
        self.__url = value

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, value: str):
        self.__username = value

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, value: str):
        self.__password = value

    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, value):
        self.__root = value

    def connect(self):
        options = {
         'webdav_hostname': self.url,
         'webdav_login':    self.username,
         'webdav_password': self.password,
         'webdav_verbose':  True, # This does nothing
         'webdav_root':     self.root
        }
        logger.info(f'Connecting to {self.url} with user {self.username}')
        self.client = wc.Client(options)

class CloudFiles(CloudConnection):
    def __init__(self, url, username, password, root):
        super().__init__(url, username, password, root)
        self.__download_queue = []
        self.__upload_queue = []

    @property
    def filter(self) -> str:
        try:
            return self.__regex
        except:
            return ''

    @filter.setter
    def filter(self, value: str):
        logger.debug(f'Setting filter: {value}')
        self.__regex = value

    @property
    def dir(self) -> str:
        try:
            return self.__dir
        except:
            return os.path.sep

    @dir.setter
    def dir(self, value: str):
        if self.client.check(value):
            self.__dir = value
            logger.info(f'Setting working directory to: {value}')
        else:
            logger.warning(f'Working directory {value} does not exist. Using root.')
            self.__dir = ''

    @property
    def absolutePaths(self) -> bool:
        try:
            return self.__absolutePaths
        except:
            return True

    @absolutePaths.setter
    def absolutePaths(self, value: bool):
        self.__absolutePaths = value

    @property
    def dirs(self) -> list:
        """All foldernames in the current directory."""
        if self.absolutePaths:
            return [os.path.join(self.dir, dir) for dir in self.client.list(self.dir)  \
                if re.search(os.path.sep, dir)]
        return [dir for dir in self.client.list(self.dir) \
            if re.search(os.path.sep, dir)]

    @property
    def files(self) -> list:
        """All filenames in the current directory."""
        if self.absolutePaths:
            return [os.path.join(self.dir, file) for file in self.client.list(self.dir) \
                if not re.search(os.path.sep, file)]
        return [file for file in self.client.list(self.dir) \
            if not re.search(os.path.sep, file)]

    @property
    def filteredFiles(self) -> list:
        """Filenames matching filter in the current directory."""
        return [Util.no_root_slash(file) for file in self.files if re.search(self.filter, file)]

    @property
    def filteredDirs(self) -> list:
        """Foldernames matching filter in the current directory."""
        return [os.path.join(self.dir, dir) for dir in self.dirs \
            if re.search(self.filter, dir)]

    def enqueue_upload(self, local_file: str, remote_file: str) -> bool:
        if not any(i['remote'] == remote_file or i['local'] == local_file for i in self.__upload_queue):
            logger.info(f'Queuing {os.path.basename(local_file)} for upload')
            self.__upload_queue.append(dict(remote=remote_file, local=local_file))
            return True
        logger.info(f'{os.path.basename(local_file)} is already in the download queue')
        return False

    def enqueue_download(self, remote_file: str, local_file: str) -> bool:
        if not any(i['remote'] == remote_file or i['local'] == local_file for i in self.__download_queue):
            self.__download_queue.append(dict(remote=remote_file, local=local_file))
            logger.info(f'Queuing {os.path.basename(remote_file)} for download')
            return True
        logger.info(f'{os.path.basename(remote_file)} is already in the download queue')
        return False

    def download(self):
        """Download all files in the queue."""
        logger.info('Starting download for {} file(s)'.format(len(self.__download_queue)))
        while self.__download_queue > []:
            file = self.__download_queue.pop()
            if not os.path.isdir(os.path.dirname(file['local'])):
                logger.debug(f'Create missing directory {os.path.dirname(file["local"])}')
                Util.local_mkdirs(os.path.dirname(file['local']), '')
            logger.info('Downloading {remote} to {local}'.format(**file))
            self.client.download_sync(remote_path=file['remote'], local_path=file['local'])
        logger.info('Finished downloading all files.')

    def upload(self):
        """Upload all files in the queue."""
        logger.info('Starting upload for {} file(s)'.format(len(self.__upload_queue)))
        while self.__upload_queue > []:
            file = self.__upload_queue.pop()
            if not self.client.check(os.path.dirname(file['remote'])):
                Util.webdav_mkdirs(os.path.dirname(file['remote']), '', self.client)
                logger.debug(f'Create missing directory {os.path.dirname(file["remote"])}')
            logger.info('Uploading {local} to {remote}'.format(**file))
            self.client.upload_sync(remote_path=file['remote'], local_path=file['local'])
        logger.info('Finished uploading all files.')
