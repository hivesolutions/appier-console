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

import os
import sys
import time
import json
import threading
import contextlib

import appier

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
        spinner = "point",
        interval = None,
        label = "Loading ",
        stream = sys.stdout,
        *args, **kwargs
    ):
        threading.Thread.__init__(self, *args, **kwargs)
        self.spinner = spinner
        self.interval = interval
        self.label = label
        self.stream = stream

    def run(self):
        threading.Thread.run(self)

        cls = self.__class__

        self.running = True

        spinners = cls.spinners()
        spinner = spinners[self.spinner]

        interval = (self.interval or spinner["interval"]) / 1000.0
        frames = spinner["frames"]
        label = appier.legacy.str(self.label)

        index = 0
        is_first = True

        while self.running:
            value = index % len(frames)
            if is_first: is_first = False
            else: self.stream.write(CLEAR_LINE + "\r")
            self.stream.write(label + frames[value])
            self.stream.flush()
            time.sleep(interval)
            index += 1

        self.stream.write(CLEAR_LINE + "\r")
        self.stream.flush()

    def stop(self):
        self.running = False

    def set_label(self, value):
        self.label = value

    @classmethod
    def spinners(cls):
        spinners_path = os.path.join(os.path.dirname(__file__), "res", "spinners.json")

        with open(spinners_path, "rb") as file:
            contents = file.read()

        contents = contents.decode("utf-8")
        return json.loads(contents)

@contextlib.contextmanager
def ctx_loader(*args, **kwargs):
    thread = LoaderThread(*args, **kwargs)
    thread.start()
    try: yield thread
    finally:
        thread.stop()
        thread.join()

if __name__ == "__main__":
    spinner = appier.conf("SPINNER", "point")
    with ctx_loader(spinner = spinner) as loader:
        time.sleep(10.0)
else:
    __path__ = []
