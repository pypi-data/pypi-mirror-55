#!/usr/bin/env python3

__all__ = ['clean']

import os
import sys
import json
from pathlib import Path

def jsonReplace(dict, key, newval):
    try:             dict[key] = newval
    except KeyError: pass

def jsonDump(file, dict):
    with open(file, 'w') as f: json.dump(dict, f, indent=1)

def clearRunCount(file):
    with open(file, 'r') as f:
        data = json.load(f)
        for cell in data["cells"]:
            jsonReplace(cell, "execution_count", None)
    jsonDump(file, data)

def clearMetaData(file):
    with open(file, 'r') as f:
        data = json.load(f)
        jsonReplace(data, "metadata", {})
    jsonDump(file, data)

def clean(file, order=True, meta=True):
    if order: clearRunCount(file)
    if meta:  clearMetaData(file)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        raise EOFError("Expected to receive a specific file name to clean")
    fn = Path(sys.argv[1])
    clean(fn)