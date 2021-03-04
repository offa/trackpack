# trackpack - Package audio tracks
#
# Copyright (C) 2020-2021  offa
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

import unittest
from trackpack import cli


class TestCli(unittest.TestCase):
    def test_prints_help_if_no_arguments_passed(self):
        with self.assertRaises(SystemExit) as context:
            cli.parse_args([])
        self.assertEqual(0, context.exception.code)

    def test_pack_command_default(self):
        args = cli.parse_args(['pack'])
        self.assertEqual("pack", args.command)
        self.assertFalse(args.pack_explicit_files)

    def test_pack_command_with_explicit_file(self):
        args = cli.parse_args(['pack', 'f0.wav', 'f1.wav'])
        self.assertEqual("pack", args.command)
        self.assertEqual(['f0.wav', 'f1.wav'], args.pack_explicit_files)

    def test_pack_with_custom_archive_name(self):
        args = cli.parse_args(['pack', "--archive-name", "xyz"])
        self.assertEqual("pack", args.command)
        self.assertEqual("xyz", args.archive_name)

    def test_pack_with_date(self):
        args = cli.parse_args(['pack', "--append-date"])
        self.assertEqual("pack", args.command)
        self.assertTrue(args.append_date)
