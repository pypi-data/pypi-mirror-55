"""Zoom CLI.
"""

import sys

import zoom


required = ['tools/zoom']

for directory in required:
    path = zoom.tools.zoompath(directory)
    if path not in sys.path:
        sys.path.insert(0, path)

print(sys.path)
from main import main

