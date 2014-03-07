# -*- coding: utf-8 -*-


"""
===================
Job Queue Consumers
===================

:Author:
    Moritz Emanuel Beber
:Date:
    2014-02-14
:Copyright:
    Copyright |c| 2014, Jacobs University Bremen gGmbH, all rights reserved.
:File:
    consumers.py

.. |c| unicode:: U+A9
"""


__all__ = ["generic_consumer"]


import logging
import cPickle as pickle


LOGGER = logging.getLogger(__name__)


def generic_consumer(queue, worker, sentinel):
    """
    Parameters
    ----------
    worker: callable
        The worker is called with a job.body and should return a result.
    queue: beanstalkc.Connection
        A beanstalkd queue connection watching and using the right tube(s).
    sentinel:
        Object that when found in the queue causes the shutdown of the consumer.

    Note
    ----
    The consumer is intended to be called on within a thread, process, or
    IPython kernel so that there are multiple entities consuming and evaluating
    jobs.

    Warning
    -------
    It is absolutely necessary that the queue is watching the correct tube(s) to
    consume jobs from and is using the right tube to submit results to.
    """
    def consume():
        try:
            job = queue.reserve()
            obj = pickle.loads(job.body)
        except (pickle.UnpicklingError, Exception) as err:
            LOGGER.error(str(err))
            job.bury()
        except (KeyboardInterrupt, SystemExit):
            LOGGER.info("shutting down")
            raise StopIteration
        if obj == sentinel: # real sentinel
            raise StopIteration
        return (job, obj)

    for (job, obj) in iter(consume, sentinel): # bogus sentinel but intended
        try:
            result = worker(**obj)
        except Exception as err:
            LOGGER.error(str(err))
            job.bury()
        except (KeyboardInterrupt, SystemExit):
            LOGGER.info("shutting down")
            job.release()
        else:
            queue.put(pickle.dumps(result))
            job.delete()

