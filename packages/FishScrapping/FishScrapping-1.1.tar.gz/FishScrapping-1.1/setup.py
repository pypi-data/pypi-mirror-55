#!/usr/bin/env python3

import setuptools
from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(name="FishScrapping",
      version='1.1',
      author='Ulises Rosas',
      long_description = readme,
      long_description_content_type = 'text/markdown',
      author_email='ulisesfrosasp@gmail.com',
      url='https://github.com/Ulises-Rosas/OBISdat',
      packages = ['FishScrapping'],
      package_dir = {'FishScrapping': 'src'},
      scripts = ['src/fishbase.py'],
      classifiers = [
             'Programming Language :: Python :: 3',
             'License :: OSI Approved :: MIT License'
             ]
      )
