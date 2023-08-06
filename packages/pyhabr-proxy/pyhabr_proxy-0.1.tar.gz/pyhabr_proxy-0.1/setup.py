"""
установка пакета pybga, в папке с setup.py ->
pip3 install --upgrade .
"""

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pyhabr_proxy',
      version='0.1',
      description='local habr.com proxy',
      long_description=long_description, 
      long_description_content_type='text/markdown',   
      author='Nikita Kuzin',
      author_email='getsense@yandex.ru',
      packages=['pyhabr_proxy'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Freeware",
        "Operating System :: OS Independent",
      ],
      zip_safe=False
)
