#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = ["libusb", "pyusb", "aenum"]

setup(
    name="pybpod-gui-plugin-soundcard",
    version='0.1.6',
    description="""PyBpod Sound card module""",
    long_description="""Library to control the Harp Sound Card board developed by the Scientific Hardware Platform at
    the Champalimaud Foundation.""",
    author="Luís Teixeira",
    author_email="micboucinha@gmail.com",
    license="MIT",
    url="https://github.com/pybpod/pybpod-gui-plugin-soundcard",
    include_package_data=True,
    packages=find_packages(),
    package_data={"pybpod_soundcard_module": ["resources/*.*"]},
    install_requires=requirements,
)
