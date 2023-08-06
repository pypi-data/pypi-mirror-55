# coding: utf-8

import yaml
import pytoml as toml
import json
import re

"""
Файты формата .md с заголовком

'''
---
key1: value1
key2: value2
---

content
'''

собирает заголовок в нужный формат
и создет структуру вида:

{
    "key1": "value1",
    "key2": "value2",
    "body": "content"
}
"""

re_splitter = re.compile("^---(?P<format>(yaml|json|toml|))\n(?P<meta>.*?)---(\n(?P<body>.*)|)$", re.MULTILINE | re.DOTALL)

new_line = "\n"


def load(stream, meta_format="yaml"):
    s = stream.read()
    return loads(s, meta_format)


def loads(string, meta_format="yaml"):
    m = re_splitter.match(string)
    d = {}
    if not m:
        return {"body": string}
    f = m.groupdict("format") if m.groupdict().get("format") else meta_format
    if f == "yaml":
        d = yaml.load(m.groupdict().get("meta"))
    elif f == "json":
        d = json.loads(m.groupdict().get("meta"))
    elif f == "toml":
        d = toml.loads(m.groupdict().get("meta"))
    if m.groupdict().get("body"):
        d["body"] = m.groupdict().get("body")
    return d


def dumps(data, meta_format="yaml"):
    body = data.pop("body", "")
    file_string = "---" + meta_format + new_line
    if meta_format == "yaml":
        file_string += yaml.dump(data, default_flow_style=False)
    elif meta_format == "json":
        file_string += json.dumps(data)
    elif meta_format == "toml":
        file_string += toml.dumps(data)
    file_string = new_line + "---" + new_line + body
    return file_string


def dump(stream, data, meta_format="yaml"):
    stream.write(dumps(data, meta_format))

