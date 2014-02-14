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


__all__ = ["DirectoryWatcher"]


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
        The dispatcher is intended to interpret the file contents and put that
        into a queue.

        Warning
        -------
        The dispatcher should be an exclusive instance for each DirectoryWatcher
        Thread, unless it is thread safe.
        """
        super(DirectoryWatcher, self).__init__(**kw_args)
        dir_path = os.path.abspath(dir_path)
        if not os.path.exists(dir_path):
            raise OSError("directory to watch does not exist")
        self.path = os.path.join(dir_path, glob_pattern)
        self.dispatch = dispatcher
        self.cache = set()
        self.wait = float(wait)

    def run(self):
        while True:
            try:
                files = self.cache.difference(set(glob(self.path)))
                self.cache.update(files)
                for filename in files:
                    self.dispatch(filename)
                time.sleep(self.wait)
            except Exception as err:
                LOGGER.error(str(err))


def watch_input(dispatcher, mode="rb", encoding="utf-8"):
    """
    Read lines from a number of files or sys.stdin and pass each line to a
    dispatcher.
    """
    for line in fileinput.input(mode=mode, openhook=fileinput.hook_compressed):
        dispatcher(codecs.decode(line, encoding))

