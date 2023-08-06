import re
import os

class Util:
    @staticmethod
    def local_mkdirs(path, root):
        """Recursive directory creation on the local storage."""
        current = os.path.join(root, path.split(os.path.sep, 1)[0])
        try:
            os.mkdir(current)
        except FileExistsError:
            pass
        try:
            next = path.split(os.path.sep, 1)[1]
        except IndexError:
            return
        if next is not '':
            Util.local_mkdirs(next, current)
        return

    @staticmethod
    def webdav_mkdirs(path, root, connection):
        """Recursive directory creation on the webdav enpoint."""
        current = os.path.join(root, path.split(os.path.sep, 1)[0])
        if not connection.check(current):
            connection.mkdir(current)
        try:
            next = path.split(os.path.sep, 1)[1]
        except IndexError:
            return
        if next is not '':
            Util.webdav_mkdirs(next, current, connection)
        return

    @staticmethod
    def get_local_files(root_dir, filter='', filter2='^[^\.]', include_root=False):
        """Walk through all dirs in the root_dir."""
        output = []
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if re.search(filter, file) and re.search(filter2, file):
                    root = root.replace(root_dir, '') if not include_root else root
                    output += [os.path.join(Util.no_root_slash(root), file)]
        return output

    @staticmethod
    def get_local_folders(root_dir, filter='', topdown=False, include_root=False):
        output = []
        for root, dirs, files in os.walk(root_dir, topdown=topdown):
            directory = root.replace(root_dir,'') if not include_root else root
            if directory is '':
                continue
            output += [directory[1:] if directory[0] is os.path.sep else directory]
        return output

    @staticmethod
    def no_root_slash(path):
        try:
            return path[1:] if path[0] is os.path.sep else path
        except IndexError:
            return ''
