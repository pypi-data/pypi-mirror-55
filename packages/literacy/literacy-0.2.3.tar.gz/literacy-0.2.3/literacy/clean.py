#!/usr/bin/env python3

__all__ = ['clean']

import os
import sys
import json
from pathlib import Path

def jsonReplace(dict, key, newval):
    try:             dict[key] = newval
    except KeyError: pass

def jsonDump(file:Path, dict):
    with open(file, 'w') as f: json.dump(dict, f, indent=1)

def clearRunCount(data:Path):
    for cell in data["cells"]:
        jsonReplace(cell, "execution_count", None)

def clearMetaData(file:Path):
    jsonReplace(data, "metadata", {})
    for cell in data["cells"]:
        jsonReplace(data, "metadata", {})

def clean(file:Path, order=True, meta=True):
    with open(file, 'r') as f:
        data = json.load(f)
        if order: clearRunCount(data)
        if meta:  clearMetaData(data)
    jsonDump(file, data)

def clean_all(folder:Path, **kwargs):
    # TODO get folder tree and find all ipynb files
    # TODO iterate and clean
    print(f"Cleaning {folder.stem} notebooks")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        raise EOFError("Expected to receive a specific file name to clean")
    fn = Path(sys.argv[1])
    clean(fn)