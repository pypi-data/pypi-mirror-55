from os import path
from setuptools import setup, find_packages

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pysportsref',
      version='0.0.2',
      packages=find_packages(),
      description='Utilities for working with Sports Reference',
      install_requires=['bs4', 'numpy', 'pandas', 'requests', 'lxml', 'tqdm'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      license='MIT',
      url='https://github.com/hwchase17/pysportsref')
