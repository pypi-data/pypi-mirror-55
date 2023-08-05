from distutils.core import setup
from setuptools import find_packages


def readme():
    with open('README.md') as f:
        return f.read()

setup(
  name = 'flask-check-json', 
  packages=find_packages(exclude=['tests.*', 'tests']),
  version = '0.1',
  license='MIT',
  description = 'JSON Validator',
  author = 'Ercy Moreira Neto',
  author_email = 'ercym.neto@gmail.com',
  url = 'https://github.com/panda-coder/flask-check-json',
  download_url = 'https://github.com/panda-coder/flask-check-json',
  keywords = ['json'],
  install_requires=[
        'flask>=1.0.2',
        'jsonschema>=3.0.1'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Framework :: Flask',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6'
  ],
)