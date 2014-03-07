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


__all__ = ["generic_handler"]


import logging
import cPickle as pickle


LOGGER = logging.getLogger(__name__)


def generic_handler(queue, handler):
    """
    Warning
    -------
    The handler queue has to watch the right tube(s).
    """
    while True:
        try:
            job = queue.reserve()
            handler(pickle.loads(job.body))
        except Exception as err:
            LOGGER.error(str(err))
            job.bury()
        except (KeyboardInterrupt, SystemExit):
            LOGGER.info("shutting down")
            break
        else:
            job.delete()

