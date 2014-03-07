#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
=========
Job Queue
=========

:Authors:
    Moritz Emanuel Beber
:Date:
    2014-02-23
:Copyright:
    Copyright |c| 2014, Jacobs University Bremen gGmbH, all rights reserved.
:File:
    setup.py

.. |c| unicode:: U+A9
"""


from setuptools import setup


setup(
    name = "jobq",
    version = "0.1",
    description = "provide convenience functions to supply and consume a"\
            " beanstalkd queue",
    author = "Moritz Emanuel Beber",
    author_email = "moritz (dot) beber (at) gmail (dot) com",
    url = "http://github.com/Midnighter/jobq",
    packages = ["jobq"],
)

