# -*- coding: utf-8 -*-


"""
===================
Job Queue Suppliers
===================

:Author:
    Moritz Emanuel Beber
:Date:
    2014-02-13
:Copyright:
    Copyright |c| 2014, Jacobs University Bremen gGmbH, all rights reserved.
:File:
    suppliers.py

.. |c| unicode:: U+A9
"""


__all__ = ["DirectoryWatcher", "watch_input"]


import os
import logging
import threading
import time
import fileinput
import codecs

from glob import glob


LOGGER = logging.getLogger(__name__)


class DirectoryWatcher(threading.Thread):

    def __init__(self, dir_path, dispatcher, glob_pattern="*", wait=1.0, **kw_args):
        """
        Watches a directory and passes files matching a pattern found there to a
        dispatcher.

        The watcher is a Thread object so that one can be started for each
        directory of interest.

        Parameters
        ----------
        dir_path: str
            Directory to be watched. This is turned into an absolute path.
        dispatcher: callable
            The dispatcher is called with a file path as an argument.
        glob_pattern: str
            The glob pattern to match files found in the directory.
        wait: float
            Time in seconds to wait between directory checks.

        Notes
        -----
        The dispatcher is intended to interpret the file contents and put them
        into a queue.

        Warning
        -------
        The dispatcher should be an exclusive instance for each DirectoryWatcher
        Thread, unless it is thread safe.
        """
        super(DirectoryWatcher, self).__init__(**kw_args)
        dir_path = os.path.abspath(dir_path)
        if not os.path.exists(dir_path):
            raise OSError("directory '%s' does not exist" % (dir_path,))
        self.path = os.path.join(dir_path, glob_pattern)
        self.dispatch = dispatcher
        self.cache = set()
        self.wait = float(wait)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

    def run(self):
        while True:
            try:
                files = set(glob(self.path)).difference(self.cache)
                self.cache.update(files)
                for filename in files:
                    LOGGER.debug("found file '%s'", filename)
                    self.dispatch(filename)
                time.sleep(self.wait)
            except Exception as err:
                LOGGER.error(str(err))
            if self.stopped():
                LOGGER.info("shutting down")
                break


def watch_input(dispatcher, mode="rb", encoding="utf-8"):
    """
    Read lines from a number of files or sys.stdin and pass each line to a
    dispatcher.
    """
    for line in fileinput.input(mode=mode, openhook=fileinput.hook_compressed):
        dispatcher(codecs.decode(line, encoding))

