#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2018 Hive Solutions Lda.
#
# This file is part of Hive Appier Framework.
#
# Hive Appier Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Appier Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Appier Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2018 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import sys
import time
import threading
import contextlib

COLOR_RESET = "\033[0m"
COLOR_WHITE = "\033[1;37m"
COLOR_BLACK = "\033[0;30m"
COLOR_BLUE = "\033[0;34m"
COLOR_LIGHT_BLUE = "\033[1;34m"
COLOR_GREEN = "\033[0;32m"
COLOR_LIGHT_GREEN = "\033[1;32m"
COLOR_CYAN = "\033[0;36m"
COLOR_LIGHT_CYAN = "\033[1;36m"
COLOR_RED = "\033[0;31m"
COLOR_LIGHT_RED = "\033[1;31m"
COLOR_PURPLE = "\033[0;35m"
COLOR_LIGHT_PURPLE = "\033[1;35m"
COLOR_BROWN = "\033[0;33m"
COLOR_YELLOW = "\033[1;33m"
COLOR_GRAY = "\033[0;30m"
COLOR_LIGHT_GRAY = "\033[0;37m"
CLEAR_LINE = "\033[K"

class LoaderThread(threading.Thread):
    """
    Thread class to be used to display the loader into
    the output stream in an async fashion.
    """

    def __init__(
        self,
        timeout = 0.08,
        label = "Loading ",
        stream = sys.stdout,
        *args, **kwargs
    ):
        threading.Thread.__init__(self, *args, **kwargs)
        self.timeout = timeout
        self.label = label
        self.stream = stream

    def run(self):
        threading.Thread.run(self)
        cls = self.__class__

        self.running = True

        frames = cls.FRAMES_5
        index = 0
        is_first = True

        while self.running:
            value = index % len(frames)
            if is_first: is_first = False
            else: self.stream.write(CLEAR_LINE + "\r")
            self.stream.write(self.label + frames[value])
            self.stream.flush()
            time.sleep(self.timeout)
            index += 1

        self.stream.write(CLEAR_LINE + "\r")
        self.stream.flush()

    def stop(self):
        self.running = False

    def set_label(self, value):
        self.label = value

    @classmethod
    def spinners(cls):
        #@todo tneho de carregar o json dos spinners
        pass

@contextlib.contextmanager
def ctx_loader(timeout = 0.08, label = "Loading ", stream = sys.stdout):
    thread = LoaderThread()
    thread.start()
    try: yield thread
    finally:
        thread.stop()
        thread.join()
