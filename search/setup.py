import os
import re

from setuptools import find_packages, setup
from pathlib import Path


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = Path.cwd() / 'search' / '__init__.py'
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            msg = 'Cannot find version in search/__init__.py'
            raise RuntimeError(msg)


install_requires = ['aiohttp']

setup(
    name='Search',
    version=read_version(),
    description='Trood Search',
    platforms=['POSIX'],
    packages=find_packages(),
    install_requires=install_requires,
    zip_safe=False
)