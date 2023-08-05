# -*- coding: utf-8 -*-
import os
from setuptools import setup

# with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
# README = readme.read()

with open("README.md", "r") as fh:
    long_description = fh.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='pyqttotp',
    version='0.9.2',
    packages=['pyqttotp'],
    include_package_data=False,
    license='Apache License version 2.0',
    description='TOTP QR Code Generator writtern in Qt.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bluszcz/pyqttotp',
    author='Rafal Zawadzki',
    author_email='bluszcz@bluszcz.net',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 2.7',
        'Topic :: Security',
        'Topic :: Security :: Cryptography'
    ],
    entry_points={
        'console_scripts': ['pyqttotp=pyqttotp.pyqttotp:main'],
    },
    install_requires=[
        'PySide2==5.13.1',
        'Pillow==6.2.1',
        'pyotp==2.3.0',
        'qrcode==6.1'
    ],
)
