# This file follows example shown at
# https://docs.python.org/3/extending/building.html#building-c-and-c-extensions-with-distutils

from distutils.core import setup, Extension

example = Extension('example',
                    sources=['examplemodule.c'])

setup(name='example',
      version='0.1',
      ext_modules=[example])
