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

import unittest
from unittest.mock import patch, call
import os
from trackpack import trackpacker


class TestTrackPack(unittest.TestCase):

    @patch("os.walk")
    def test_discover_audiofiles_returns_audio_files(self, walk_mock):
        walk_mock.return_value = _create_walk_files(['proj stem2.wav', 'proj stem4.wav',
                                                     'proj stem1.wav', 'proj.wav',
                                                     'proj stem3.wav'])

        (master, stems) = trackpacker.discover_audiofiles("proj", "/tmp/export")
        walk_mock.assert_called_with('/tmp/export')
        self.assertEqual('proj.wav', master)
        self.assertListEqual(['proj stem2.wav', 'proj stem4.wav',
                              'proj stem1.wav', 'proj stem3.wav'], stems)

    @patch("os.walk")
    def test_discover_audiofiles_returns_only_related_audio_files(self, walk_mock):
        walk_mock.return_value = _create_walk_files(['proj stem2.wav', 'ignore.txt',
                                                     'proj stem1.wav', 'proj.wav', 'archive.zip',
                                                     "proj unrelated.mp3"])

        (_, stems) = trackpacker.discover_audiofiles("proj", "/tmp/export")
        self.assertListEqual(['proj stem2.wav', 'proj stem1.wav'], stems)

    @patch("os.walk")
    def test_discover_audiofiles_master_track_matches_project_name(self, walk_mock):
        walk_mock.return_value = _create_walk_files(['example.wav', 'proj stem4.wav',
                                                     'proj stem1.wav', 'proj.wav',
                                                     'proj stem3.wav'])
        (master, _) = trackpacker.discover_audiofiles("example", "/tmp/export")
        self.assertEqual('example.wav', master)

    @patch("os.walk")
    def test_discover_audiofiles_fails_if_no_master(self, walk_mock):
        walk_mock.return_value = _create_walk_files(['proj stem1.wav', 'proj stem2.wav'])

        with self.assertRaises(trackpacker.MissingFileException):
            trackpacker.discover_audiofiles("proj", "/tmp/export")

    @patch("os.walk")
    def test_discover_audiofiles_fails_if_no_stems(self, walk_mock):
        walk_mock.return_value = _create_walk_files(["proj.wav"])

        with self.assertRaises(trackpacker.MissingFileException):
            trackpacker.discover_audiofiles("proj", "/tmp/export")

    @patch("trackpack.trackpacker.ZipFile", autospec=True)
    # pylint: disable=R0201
    def test_pack_files_creates_archive_of_stems(self, zip_mock):
        trackpacker.pack_files("/tmp/proj/Exports", "projname",
                               "archivename", ["a.wav", "b.wav", "c.wav"])
        zip_mock.assert_has_calls(_create_zip_mock_calls("archivename", "/tmp/proj/Exports", {
            "a.wav": "a.wav",
            "b.wav": "b.wav",
            "c.wav": "c.wav"
        }))

    @patch("trackpack.trackpacker.ZipFile", autospec=True)
    # pylint: disable=R0201
    def test_pack_files_removes_project_name_from_stems(self, zip_mock):
        trackpacker.pack_files("/tmp/x", "proj1", "archive1",
                               ["proj1 a.wav", "b.wav", "proj1 c.wav"])
        zip_mock.assert_has_calls(_create_zip_mock_calls("archive1", "/tmp/x", {
            "proj1 a.wav": "a.wav",
            "b.wav": "b.wav",
            "proj1 c.wav": "c.wav"
        }))

    @patch("trackpack.trackpacker.ZipFile", autospec=True)
    # pylint: disable=R0201
    def test_pack_files_replaces_blanks_in_names(self, zip_mock):
        trackpacker.pack_files("/tmp/x", "proj1", "archive1",
                               ["proj1 a a a.wav", "b 123.wav", "proj1   c d efg.wav"])
        zip_mock.assert_has_calls(_create_zip_mock_calls("archive1", "/tmp/x", {
            "proj1 a a a.wav": "a-a-a.wav",
            "b 123.wav": "b-123.wav",
            "proj1   c d efg.wav": "c-d-efg.wav"
        }))


def _create_walk_files(files):
    return iter([('proj_export_dir', [], files)])


def _create_zip_mock_calls(archive_name, proj_export_dir, files):
    call_list = [call(os.path.join(proj_export_dir, "{}.zip".format(archive_name)), "w"),
                 call().__enter__()]

    for name, entry in files.items():
        call_list.append(call().__enter__().write(os.path.join(proj_export_dir, name), entry))
    call_list.append(call().__exit__(None, None, None))

    return call_list
