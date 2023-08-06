#!python3

from setuptools import setup


setup(name='mrm',
      version='0.1.0',
      packages=['mrm'],
      entry_points={
          'console_scripts': [
              'mrm = mrm.app:main'
          ]
      },
      )
