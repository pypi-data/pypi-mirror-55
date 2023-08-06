# Copyright 2019 Christian Lölkes
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""Convert video files from one WebDAV to another WebDAV folder.

Usage:
  webdavconvert [options]
  webdavconvert (--save | --load) FILE [options]
  webdavconvert (-h | --help | --version)

Arguments:
  FILE                      Configuration file.

Options:
  -h --help                 Show this screen.
  --version                 Show version.
  --loglevel LEVEL          Set a specific log level. [default: INFO]

Target options:
  --target-url TURL         Url for the target WebDAV host. [default: https://cloud.example.com]
  --target-user TUSER       User for the target WebDAV host. [default: username]
  --target-password TPW     Password for the target user. [default: foobar]
  --target-dir TDIR         Directory to store files. [default: /]
  --target-root TROOT       Root of the WebDAV host. [default: /public.php/webdav/]

Source options:
  --source-url SURL         Url for the target WebDAV host. [default: https://cloud.example.com]
  --source-user SUSER       User for the target WebDAV host. [default: username]
  --source-password SPW     Password for the source user. [default: foobar]
  --source-dir SDIR         Directory to store files in [default: /]
  --source-root SROOT       Root of the WebDAV host. [default: /public.php/webdav/]
  --source-filter SFILTER   Only convert files matching this regex. [default: mp4]
  --source-recursive        Recursivly browse all folders.

Convert options:
  --output-format FORMAT    Video output format. [default: mp4]
  --output-timecode         Overlay the video with the timecode.
  --output-height HEIGHT    Resize the video while keeping proportions to HEIGHT. [default: 480]
  --output-prefix PREFIX    Add this prefix to the output filename. [default: ]
  --output-suffix SUFFIX    Add this suffix to the output filename. [default: ]

System options:
  --ffmpeg-path PATH        Path to the ffmpeg executable. [default: /usr/local/bin/ffmpeg]

Config options:
  --save                    Overwrite the existing configuration file.
  --load                    Load the configuration file and ignore all other parameters.

"""


VERSION = '1.0.0'

### configparser ###
import configparser
config = configparser.ConfigParser()

### docopt ###
from docopt import docopt
arguments = docopt(__doc__, version=VERSION)

### Logging ###
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=getattr(logging, arguments['--loglevel'])
)
logger = logging.getLogger(__name__)
logger.debug('Hello world!')

from .WebDAV import *
from .Converter import *

def write_configuration(arguments):
    sections = ['target', 'source', 'output', 'ffmpeg']
    for section in sections:
        config[section] = {}
    for argument, value in arguments.items():
        if any(element in sections for element in argument[2:].split('-')):
            category = argument[2:].split('-')[0]
            option = argument[2:].split('-')[1]
            config[category][option] = str(value)
    with open(arguments['FILE'], 'w') as configfile:
        config.write(configfile)
        logger.info(f'Saving configuration to {arguments["FILE"]}')

if __name__ == '__main__':
    if arguments['--load']:
        config.read(arguments['FILE'])
        logger.info(f'Loading configuration from {arguments["FILE"]}')
    elif arguments['--save']:
        write_configuration(arguments)
        quit()
    else:
        quit()
    source = CloudFiles(
        config['source']['url'], config['source']['user'],
        config['source']['password'], config['source']['root'])
    target = CloudFiles(
        config['target']['url'], config['target']['user'],
        config['target']['password'], config['target']['root'])
    source.dir = config['source']['dir']
    target.dir = config['target']['dir']
    source.filter = config['source']['filter'] # '(i\d{4})|(mp4)'

    converter = Converter(source, target)
    converter.get_files_to_download(source.filter)
    converter.download_files()
    converter.convert()
    converter.get_files_to_upload(source.filter)
    converter.upload_files()
    converter.cleanup()
