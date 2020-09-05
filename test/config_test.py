# trackpack - Package audio tracks
#
# Copyright (C) 2020  offa
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

import datetime
import unittest
from trackpack import config


class TestConfig(unittest.TestCase):

    def test_default_config(self):
        cfg = config.Config()
        self.assertEqual("unnamed", cfg.name)
        self.assertEqual("unnamed", cfg.archive_name)
        self.assertEqual("Export", cfg.export_dir)
        self.assertFalse(cfg.append_date)

    def test_extension_is_stripped_from_archivename(self):
        cfg = config.Config()
        cfg.archive_name = "stems.zip"
        self.assertEqual("stems", cfg.archive_name)

    def test_append_date_appends_date_to_archive_name(self):
        today = datetime.date.today().strftime('%Y-%m-%d')

        cfg = config.Config()
        cfg.archive_name = "xyz"
        cfg.append_date = True
        self.assertEqual("xyz-{}".format(today), cfg.archive_name)

    def test_load_from_yaml(self):
        cfg = config.Config()
        cfg.load_from_yaml("name: project-1")
        self.assertEqual("project-1", cfg.name)
        self.assertEqual("project-1", cfg.archive_name)
        self.assertEqual("Export", cfg.export_dir)
        self.assertFalse(cfg.append_date)

        cfg = config.Config()
        cfg.load_from_yaml("name: project-1\narchive: proj1")
        self.assertEqual("proj1", cfg.archive_name)

        cfg = config.Config()
        cfg.load_from_yaml("name: project-1\narchive: proj1\nappend_date: true")
        self.assertTrue(cfg.append_date)
