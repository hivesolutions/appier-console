#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Appier Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import unittest

import appier

import appier_console

class BaseTest(unittest.TestCase):

    def test_colored(self):
        result = appier_console.colored("Hello World", force = True)
        self.assertEqual(result, "\x1b[0;31mHello World\x1b[0m")

        result = appier_console.colored(
            "Hello World",
            color = appier_console.COLOR_BLUE,
            force = True
        )
        self.assertEqual(result, "\x1b[0;34mHello World\x1b[0m")

        result = appier_console.colored(
            "你好世界",
            color = appier_console.COLOR_BLUE,
            force = True
        )
        self.assertEqual(result, "\x1b[0;34m你好世界\x1b[0m")

    def test_table(self):
        result = appier_console.table({
            "Microsoft" : "Bill Gates",
            "Apple" : "Steve Jobs",
            "Tesla" : "Elon Musk",
            "Amazon" : "Jeff Bezos"
        })
        self.assertEqual(result, appier.legacy.u("--------------------------\n| Amazon    | Jeff Bezos |\n| Apple     | Steve Jobs |\n| Microsoft | Bill Gates |\n| Tesla     | Elon Musk  |\n--------------------------"))

        result = appier_console.table([
            ["Microsoft", "Bill Gates"],
            ["Apple", "Steve Jobs"],
            ["Tesla", "Elon Musk"],
            ["Amazon", "Jeff Bezos"]
        ])
        self.assertEqual(result, appier.legacy.u("--------------------------\n| Amazon    | Jeff Bezos |\n| Apple     | Steve Jobs |\n| Microsoft | Bill Gates |\n| Tesla     | Elon Musk  |\n--------------------------"))

        result = appier_console.table([
            ["Microsoft", "Bill Gates"],
            ["Apple", "Steve Jobs"],
            ["Tesla", "Elon Musk"],
            ["Amazon", "Jeff Bezos"],
            ["Hello", "你好世界"]
        ])
        self.assertEqual(result, appier.legacy.u("--------------------------\n| Amazon    | Jeff Bezos |\n| Apple     | Steve Jobs |\n| Hello     | 你好世界       |\n| Microsoft | Bill Gates |\n| Tesla     | Elon Musk  |\n--------------------------"))
