#!/usr/bin/env python

from distutils.core import setup

setup(name='solavis',
      version='0.1a1.dev001',
      description='lightweight async crawler framework',
      author='JunWang',
      author_email='jstzwj@aliyun.com',
      license="MIT",
      keywords="crawler",
      url='https://github.com/jstzwj/solavis.git',
      packages=['solavis',
            'solavis.core',
            'solavis.contrib',
            'solavis.util'],
      install_requires=[
            'lxml==4.3.3',
            'requests==2.21.0',
            'aiohttp==3.6.2',
            'aiosqlite==0.10.0'
      ],
      python_requires='>=3.7',
     )