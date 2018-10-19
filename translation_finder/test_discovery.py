# -*- coding: utf-8 -*-
#
# Copyright © 2018 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate translation-finder
# <https://github.com/WeblateOrg/translation-finder>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from .finder import Finder, PurePath
from .discovery import GettextDiscovery, QtDiscovery, AndroidDiscovery, OSXDiscovery


class DiscoveryTestCase(TestCase):
    def get_finder(self, paths):
        return Finder(PurePath("."), [PurePath(path) for path in paths])

    def assert_discovery(self, first, second):
        def sort_key(item):
            return item["filemask"]

        self.assertEqual(sorted(first, key=sort_key), sorted(second, key=sort_key))


class GetttetTest(DiscoveryTestCase):
    def test_basic(self):
        discovery = GettextDiscovery(
            self.get_finder(["locales/cs/messages.po", "locales/de/messages.po"])
        )
        self.assert_discovery(
            discovery.discover(),
            [
                {
                    "filemask": "locales/*/messages.po",
                    "file_format": "po",
                    "template": None,
                }
            ],
        )

    def test_filename(self):
        discovery = GettextDiscovery(
            self.get_finder(["locales/cs.po", "locales/de.po"])
        )
        self.assert_discovery(
            discovery.discover(),
            [{"filemask": "locales/*.po", "file_format": "po", "template": None}],
        )


class QtTest(DiscoveryTestCase):
    def test_basic(self):
        discovery = QtDiscovery(self.get_finder(["ts/cs.ts", "ts/zh_CN.ts"]))
        self.assert_discovery(
            discovery.discover(),
            [{"filemask": "ts/*.ts", "file_format": "ts", "template": None}],
        )


class AndroidTest(DiscoveryTestCase):
    def test_basic(self):
        discovery = AndroidDiscovery(
            self.get_finder(
                [
                    "app/src/res/main/values/strings.xml",
                    "app/src/res/main/values-it/strings.xml",
                    "app/src/res/main/values-it/strings-other.xml",
                ]
            )
        )
        self.assert_discovery(
            discovery.discover(),
            [
                {
                    "filemask": "app/src/res/main/values-*/strings.xml",
                    "file_format": "aresource",
                    "template": "app/src/res/main/values/strings.xml",
                }
            ],
        )


class OSXTest(DiscoveryTestCase):
    def test_basic(self):
        discovery = OSXDiscovery(
            self.get_finder(
                [
                    "App/Resources/en.lproj/Localizable.strings",
                    "App/Resources/en.lproj/Other.strings",
                    "App/Resources/ru.lproj/Third.strings",
                ]
            )
        )
        self.assert_discovery(
            discovery.discover(),
            [
                {
                    "filemask": "App/Resources/*.lproj/Localizable.strings",
                    "file_format": "strings",
                    "template": "App/Resources/en.lproj/Localizable.strings",
                },
                {
                    "filemask": "App/Resources/*.lproj/Other.strings",
                    "file_format": "strings",
                    "template": "App/Resources/en.lproj/Other.strings",
                },
            ],
        )
