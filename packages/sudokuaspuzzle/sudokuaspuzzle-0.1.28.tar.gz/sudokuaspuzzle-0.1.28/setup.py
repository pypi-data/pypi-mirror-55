#!/usr/bin/env python3
from setuptools import setup
import os
import sys

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='sudokuaspuzzle',
      version='0.1.28',
      description='Customizable Sudoku',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='http://gnu.kekbay.gr/sudokuaspuzzle/versions',
        project_urls={
        'Source': 'https://gitlab.com/xoristzatziki/sudokuaspuzzle',
      },
      author='Ηλίας Ηλιάδης',
      author_email='iliadis@kekbay.gr',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment :: Puzzle Games',
      ],
      license='GPLv3',
      packages=['sudokuaspuzzle'],
      include_package_data=True,
      entry_points = {
        'console_scripts': [
            'sudokuaspuzzleC = sudokuaspuzzle.entrypoint:main'],
        'gui_scripts': [
            'sudokuaspuzzle = sudokuaspuzzle.entrypoint:main',
        ]
      },
      zip_safe=False)
