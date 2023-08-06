"""
make modules a little bit easier to use.
"""
import re as _re

from bs4 import BeautifulSoup as _BeautifulSoup


class BeautifulSoup(_BeautifulSoup):
    
    def __init__(self, ifile, ftype='file', parser='html.parser', **kwargs):
        if ftype == 'file':
            from . import read_and_write_basic
            html = read_and_write_basic.read_file(ifile)
        else:
            # ftype is 'str' or 'string'
            html = ifile
        
        super().__init__(html, parser, **kwargs)
    
    def insert_before(self, successor):
        pass
    
    def insert_after(self, successor):
        pass


class Regex:
    exp = None
    
    def compile(self, exp):
        self.exp = _re.compile(exp)
        return self

    # ------------------------------------------------
    
    def _find(self, x, pos: int):
        try:
            return self.exp.findall(x)[pos]
        except AttributeError:
            return None
    
    def find(self, x):
        return self._find(x, 0)
    
    def find_last(self, x):
        return self._find(x, -1)

    def find_all(self, x):
        return self.exp.findall(x)

    # ------------------------------------------------

    @staticmethod
    def sub(a, b, c):
        return _re.sub(a, b, c)


re = Regex()
