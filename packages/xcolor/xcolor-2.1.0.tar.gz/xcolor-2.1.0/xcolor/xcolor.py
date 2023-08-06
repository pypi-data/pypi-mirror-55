import sys
import functools
from .colors import *


class Color:

    def __init__(self, color="Default", style="Default"):
        self.color = color
        self.style = style

    def print(self, *objects, sep=' ', end='\n', file=sys.stdout, flush=False):
        print('\033[%s;%sm' % (Style.__dict__[self.style.lower()], Foreground.__dict__[self.color.lower()]), end='',
              flush=True)
        print(*objects, sep=sep, end='', file=file, flush=flush)
        print('\033[0m', end=end, flush=True)

    def __call__(self, func):
        @functools.wraps(func)
        def wrap(*args, **kwargs):
            print('\033[%s;%sm' % (Style.__dict__[self.style.lower()], Foreground.__dict__[self.color.lower()]), end='',
                  flush=True)
            value = func(*args, **kwargs)
            print('\033[0m', end='', flush=True)
            return value

        return wrap

    def setenv(self):
        print('\033[%s;%sm' % (Style.__dict__[self.style.lower()], Foreground.__dict__[self.color.lower()]), end='',
              flush=True)

    @classmethod
    def clear(cls):
        print('\033[0m', end='', flush=True)

    def __getattr__(self, item):
        if isinstance(item, str):
            return item.title()

    def __repr__(self):
        return "<Color('%s','%s')>" % (self.color.title(), self.style.title())


def clear():
    print('\033[0m', end='', flush=True)
