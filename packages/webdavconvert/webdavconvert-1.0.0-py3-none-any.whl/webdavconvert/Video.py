import subprocess
import os
import re
import logging
from .Util import *

logger = logging.getLogger(__name__)

class Video:
    FFPROBE = subprocess.check_output(['which', 'ffprobe']).decode().rstrip('\n')
    FFMPEG = subprocess.check_output(['which', 'ffmpeg']).decode().rstrip('\n')

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.__video_filter = []
        self.ffmpeg_options =  ['-y','-loglevel', 'quiet'] # '-stats'
        self.convert_options = ['-vcodec', 'libx264', '-acodec', 'aac', \
            '-pix_fmt', 'yuv420p', '-map', '0:1', '-map', '0:0', \
            '-write_tmcd', 'off', '-movflags', 'faststart']
            # '-preset', 'slow', '-crf', '22'
        pass

    @property
    def video_font(self) -> str:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), \
            'font', 'Inconsolata-Regular.ttf')

    def convert(self):
        """Run the ffmpeg command"""
        if not os.path.isdir(os.path.dirname(self.output_file)):
            logger.debug(f'Create missing directory {os.path.dirname(self.output_file)}')
            Util.local_mkdirs(os.path.dirname(self.output_file), '')
        command = [Video.FFMPEG] \
            + ['-i', self.input_file] \
            + self.convert_options \
            + self.ffmpeg_options \
            + self.video_filter + \
            [self.output_file]
        logger.debug(' '.join(command))
        logger.info('Starting video conversion')
        try:
            result = subprocess.check_output(command)
            logger.info(f'Video conversion successful for {self.output_file}')
            return True
        except Exception as e:
            logger.error(e)
            return False

    @property
    def filter_timecode(self) -> str:
        filter = f'drawtext=fontfile={self.video_font}:' \
            + 'fontsize=h/6:fontcolor=white:' \
            + f"timecode='00\\:00\\:00\\:00':r={self.fps}:" \
            + 'x=(w-tw)/2:y=h-(2*lh):box=1:boxcolor=0x00000000@1'
        return filter

    def filter_height(self, value) -> str:
        return f'scale={value}:-2'

    def add_video_filter(self, filter: list):
        self.__video_filter += [filter]

    @property
    def video_filter(self) -> list:
        if self.__video_filter > []:
            for filter in self.__video_filter:
                logger.info(f'ffmpeg filter option: {filter}')
            return ['-vf', ','.join(self.__video_filter)]
        return []

    @property
    def input_ext(self):
        return os.path.splitext(self.input_file)[1]

    @property
    def output_ext(self):
        try:
            return self.__output_ext
        except:
            return self.input_ext

    @output_ext.setter
    def output_ext(self, value):
        self.__output_ext = value
        self.output_file = self.output_file

    @property
    def output_file(self):
        return self.__output_file

    @output_file.setter
    def output_file(self, value):
        self.__output_file = os.path.splitext(value)[0] + self.output_ext

    @property
    def fps(self):
        """Return the FPS of this files"""
        options = ['-v', 'error', '-select_streams', 'v', '-of', \
            'default=noprint_wrappers=1:nokey=1', '-show_entries', \
            'stream=r_frame_rate']
        command = [Video.FFPROBE] + options + [self.input_file]
        # Ask Joe to write custom parser
        return eval(subprocess.check_output(command).decode().rstrip('\n'))
