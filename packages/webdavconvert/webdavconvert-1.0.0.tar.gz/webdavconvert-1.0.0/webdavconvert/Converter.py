from .Video import *
from .Util import *
import logging
import os

logger = logging.getLogger(__name__)


class Converter:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.local_download_dir = 'input'
        self.local_upload_dir = 'output'

    def cleanup(self) -> None:
        logger.info('Cleaning up...')
        files_to_delete = Util.get_local_files(self.local_upload_dir, '', '', True)
        files_to_delete += Util.get_local_files(self.local_download_dir, '', '', True)
        for file in files_to_delete:
            logger.info(f'Removing local file {file}')
            os.remove(file)

        for directory in Util.get_local_folders(self.local_download_dir, ''):
            dir_path = os.path.join(self.local_download_dir, directory)
            logger.info(f'Removing local directory {dir_path}')
            os.rmdir(dir_path)

        for directory in Util.get_local_folders(self.local_upload_dir, ''):
            dir_path = os.path.join(self.local_upload_dir, directory)
            logger.info(f'Removing local directory {dir_path}')
            os.rmdir(dir_path)

    def get_files_to_download(self, filter: str) -> None:
        self.source.filter = filter
        self.__to_download = self.source.filteredFiles
        self.check_source_target()

    def get_files_to_upload(self, filter='') -> None:
        self.__to_upload = Util.get_local_files(self.local_upload_dir, filter)

    def check_source_target(self) -> None:
        self.__to_download = [f for f in self.__to_download if not self.target.client.check(f)]

    def download_files(self) -> None:
        """Download all files in the queue"""
        for remote_file in self.__to_download:
            local_target = os.path.join(self.local_download_dir, remote_file)
            self.source.enqueue_download(remote_file, local_target)
        self.source.download()

    def upload_files(self) -> None:
        """Upload all files in the queue"""
        for local_file in self.__to_upload:
            remote_target = local_file # os.path.join('/' + local_file)
            local_file = os.path.join(self.local_upload_dir, local_file)
            self.target.enqueue_upload(local_file, remote_target)
        self.target.upload()

    def convert(self) -> None:
        """Convert files using ffmpeg"""
        for file in Util.get_local_files(self.local_download_dir, self.source.filter):
            input = os.path.join(self.local_download_dir, file)
            output = os.path.join(self.local_upload_dir, file)
            video = Video(input, output)
            video.add_video_filter(video.filter_height(480))
            video.add_video_filter(video.filter_timecode)
            video.output_ext = '.mp4'
            video.convert()
