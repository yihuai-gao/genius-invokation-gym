#!/usr/bin/env python
import setuptools

def _get_version():
    with open('__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                g = {}
                exec(line, g)
                return g['__version__']
        raise ValueError('`__version__` not defined')

VERSION = _get_version()

setuptools.setup(name='gisim',
      version=VERSION,
      description='Genious Invokation Simulator',
      author='David Gao',
      author_email='davidgao1013@gmail.com',
      packages=setuptools.find_packages(),
     )