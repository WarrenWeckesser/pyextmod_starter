from distutils.core import setup, Extension

example = Extension('example',
                    sources=['examplemodule.c'])

setup(name='example',
      version='0.1',
      ext_modules=[example])
