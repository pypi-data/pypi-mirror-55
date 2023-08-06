# coding: utf-8

import os.path


class Path(object):
    def __init__(self, ct_root="/", fs_root="/"):
        self.ct_root = ct_root
        self.fs_root = fs_root

    def get(self, ct_target=None, fs_target=None):
        return PathObject(self, ct_target=ct_target, fs_target=fs_target)


class PathObject(object):
    """
    Создает объект пути
    """
    def __init__(self, path, ct_target=None, fs_target=None):
        """
        Конструктор
        :param path: путь
        :param ct_target: относительный или абсолютный путь от CT
        :param fs_target: относительный или абсолютный путь от FS
        """
        self.path = path
        if fs_target:
            self.target = fs_target
            self.type = "fs"
        else:
            self.target = ct_target
            self.type = "ct"

        self.abs = os.path.isabs(self.target)

    @property
    def fs(self):
        if self.type == "fs":
            if self.abs:
                return os.path.normpath(self.target)
            else:
                return os.path.normpath(os.path.join(self.path.fs_root, self.target))
        else:  # ct
            if self.abs:
                return os.path.normpath(os.path.join(self.path.fs_root, os.path.relpath(self.target, self.path.ct_root)))
            else:
                return os.path.normpath(os.path.join(self.path.fs_root, os.path.relpath(os.path.join(self.path.ct_root, self.target), self.path.ct_root)))

    @property
    def ct(self):
        if self.type == "fs":
            if self.abs:
                return os.path.normpath(os.path.join(self.path.ct_root, os.path.relpath(self.target, self.path.fs_root)))
            else:
                return os.path.normpath(os.path.join(self.path.ct_root, os.path.relpath(os.path.join(self.path.fs_root, self.target), self.path.fs_root)))
        else:  # ct
            if self.abs:
                return os.path.normpath(self.target)
            else:
                return os.path.normpath(os.path.join(self.path.ct_root, self.target))

    @property
    def fs_rel(self):
        return os.path.relpath(self.fs, self.path.fs_root)

    @property
    def ct_rel(self):
        return os.path.relpath(self.ct, self.path.ct_root)