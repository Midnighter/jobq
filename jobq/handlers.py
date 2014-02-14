# -*- coding: utf-8 -*-


"""
========================
Job Queue Result Manager
========================

:Author:
    Moritz Emanuel Beber
:Date:
    2014-02-14
:Copyright:
    Copyright |c| 2014, Jacobs University Bremen gGmbH, all rights reserved.
:File:
    managers.py

.. |c| unicode:: U+A9
"""


__all__ = ["generic_manager"]


import logging
import cPickle as pickle


LOGGER = logging.getLogger(__name__)


def generic_manager(handler, queue, sentinel):
    """
    Warning
    -------
    The handler queue has to watch the right tube(s).
    """
    while True:
        try:
            job = queue.reserve()
            handler(pickle.loads(job.body))
        except StandardError as err:
            LOGGER.error(str(err))
            job.bury()
        else:
            job.delete()

