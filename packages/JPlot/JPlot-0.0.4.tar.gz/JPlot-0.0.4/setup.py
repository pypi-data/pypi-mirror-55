#!/usr/bin/env python

from distutils.core import setup
from glob import glob
from src import __version__


setup(name='JPlot',
      version=__version__,
      description='A Python library for generating publication ready figures',
      # Chose a license from here: https://help.github.com/articles/licensing-a-repository
      license='MIT',
      author='Juncheng Yang',
      author_email='juncheny@cs.cmu.edu',
      packages=['src', "src.const", "src.styles"],
      data_files=[('styles', glob('src/styles/*', )), ],
      # Provide either the link to your github or to your website
      url='https://github.com/1a1a11a/JPlot',
      keywords=['plot', 'easy', ],   # Keywords that define your package best
      # install_requires=['matplotlib',
      #                   'numpy',
      #                   ],
      classifiers=[
          # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      )


# rm -r dist; python3 setup.py sdist; twine upload dist/*
