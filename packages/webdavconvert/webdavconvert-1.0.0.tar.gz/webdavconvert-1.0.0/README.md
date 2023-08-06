# webdavconvert

# Installation

```
pip install webdavconvert
```

# CLI Usage

First create a settings file with
```
python -m webdavconvert --save settings.ini
```
After setting all parameters in settings.ini you can run it with
```
python -m webdavconvert --load settings.ini
```
You can also directly run webdavconvert by setting all options through the CLI. Mixing save presets and command line options is not supported at the time, if you use ```--load``` all CLI options are ignored.

# Available commands
```
$ python -m webdavconvert -h

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
  --target-password TPW     Password for the target user. [default: password]
  --target-dir TDIR         Directory to store files. [default: /]
  --target-root TROOT       Root of the WebDAV host. [default: /public.php/webdav/]

Source options:
  --source-url SURL         Url for the target WebDAV host. [default: https://cloud.example.com]
  --source-user SUSER       User for the target WebDAV host. [default: username]
  --source-password SPW     Password for the source user. [default: password]
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

```

# As Python module

```
source = CloudFiles(url, user, password, root)
target = CloudFiles(url, user, password, root)
source.dir = ''
target.dir = ''
source.filter = 'mp4'

converter = Converter(source, target)
converter.get_files_to_download(source.filter)
converter.download_files()
converter.convert()
converter.get_files_to_upload(source.filter)
converter.upload_files()
converter.cleanup()
```
