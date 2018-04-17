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

import time

from . import base
from . import util

CONSOLE_THRESHOLD = 1024 * 1024
""" The threshold in bytes to be used to print content
in an interactive/console based download """

TEXT_THRESHOLD = 10 * 1024 * 1024
""" The threshold in bytes to be used to print content
in an text based download """

def http_callbacks(
    name,
    console_threshold = CONSOLE_THRESHOLD,
    text_threshold = TEXT_THRESHOLD
):

    with base.ctx_loader() as loader:

        status = dict(
            length = -1,
            received = 0,
            flushed = 0,
            threshold = 0,
            percent = 0.0,
            start = None
        )

        def callback_init(connection):
            loader.set_template("[%s] Establishing connection " % name)

        def callback_open(connection):
            loader.set_template("[%s] Connection established " % name)

        def callback_headers(headers):
            _length = headers.get("content-length", None)
            if _length == None: _length = "-1"
            status["length"] = int(_length)
            status["received"] = 0
            status["flushed"] = 0
            status["percent"] = 0.0
            status["threshold"] = console_threshold if util.is_tty() else text_threshold
            status["start"] = time.time()

        def callback_data(data):
            status["received"] += len(data)
            if not status["length"] == -1:
                status["percent"] = float(status["received"]) / float(status["length"]) * 100.0
          #  if status["received"] - status["flushed"] < status["threshold"]: return
            status["flushed"] = status["received"]
            output()

        def callback_result(result):
            status["percent"] = 100.0
            output()
            #try:
            #    sys.stdout.write("\n" if is_tty() else "")
            #    sys.stdout.flush()
            #except: pass

        def output():
            delta = time.time() - status["start"]
            if delta == 0.0: delta = 1.0
            speed = float(status["received"]) / float(delta) / (1024 * 1024)
            prefix = "\r" if util.is_tty() else ""
            suffix = "" if util.is_tty() else "\n"
            loader.set_template(prefix + "[%s] %.02f%% %.02fMB/s " % (name, status["percent"], speed) + suffix)

    return dict(
        callback_init = callback_init,
        callback_open = callback_open,
        callback_headers = callback_headers,
        callback_data = callback_data,
        callback_result = callback_result
    )
