# coding:utf-8

import yaml
import pytoml as toml
import json
import re
import os.path


class DataFile(object):
    """
    Работает с yaml / json / toml / md как с единым файлом
    """
    re_data_pattern = re.compile("^(.*).(yaml|json|toml)$", re.IGNORECASE)

    def __init__(self, path, data_formats=None):
        data_formats = ["yaml", "json", "toml", "md"] if not data_formats else data_formats
        m = self.re_data_pattern.match(path)
        self.data = {}
        for f in data_formats:
            if os.path.exists(m.groups()[0] + f):
                self.type = f
                with open(self.path) as file:
                    getattr(self, "__load_"+f)(file)

        if not self.file_exists():
            self.type = m.groups()[1]
        self.path = m.groups()[0] + "." + self.type

    def __load_yaml(self, file):
        self.data = yaml.safe_load(file)

    def __load_json(self, file):
        self.data = json.load(file)

    def __load_toml(self, file):
        self.data = toml.load(file)

    def __save_yaml(self, file):
        yaml.safe_dump(self.data, file)

    def __save_json(self, file):
        json.dump(self.data, file)

    def __save_toml(self, file):
        toml.dump(self.data, file)

    def save(self):
        if not self.file_exists():
            return
        with open(self.path, 'w') as file:
            getattr(self, "__save_" + self.type)(file)

    def file_exists(self):
        if self.type:
            return True
        return False

    def get(self, key, default):
        return self.data.get(key, default)

    def __getitem__(self, key):
        return self.data.get(key, None)

    def __contains__(self, item):
        return item in self.data
