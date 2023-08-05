#!/usr/bin/env python

import os
from setuptools import setup

from supaharrisclient import __version__


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(name='supaharrisclient',
      version=__version__,
      description='API client for the supaharris.com globular & star cluster database',
      author='Timo Halbesma',
      author_email='halbesma@MPA-Garching.MPG.DE',
      license='AGPL-3.0',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      url='https://github.com/tlrh314/supaharris-client',
      package_dir = {'supaharrisclient/': ''},
      packages=['supaharrisclient',],
      install_requires=[
          'numpy', 'requests',
      ],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Database :: Front-Ends',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics']
      )
