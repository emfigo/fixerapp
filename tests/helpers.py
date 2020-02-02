from io import StringIO
from unittest.mock import patch

class PrintCapture:
    _patcher = None
    _out = None

    def __init__(self, line_filter='ERROR'):
        self.line_filter = line_filter

    def __enter__(self):
        self._patcher = patch("sys.stdout", new_callable=StringIO)
        self._out = self._patcher.start()
        return self

    def __exit__(self, *args):
        self._patcher.stop()

    @property
    def lines(self):
        self._out.seek(0)
        return [
            line.rstrip("\n")
            for line in self._out.readlines()
            if self.line_filter in line
        ]

