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
from unittest.mock import patch, call
import os
from trackpack.trackpacker import TrackPacker, MissingFileException


class TestTrackPack(unittest.TestCase):
    @patch("os.walk")
    def test_discover_audiofiles_returns_audio_files(self, walk_mock):
        walk_mock.return_value = _create_walk_files(
            ['proj stem2.wav', 'proj stem4.wav', 'proj stem1.wav', 'proj.wav', 'proj stem3.wav'])

        trackpacker = TrackPacker("proj", "/tmp/export")
        (master, stems) = trackpacker.discover_audiofiles()
        walk_mock.assert_called_with('/tmp/export')
        self.assertEqual('proj.wav', master)
        self.assertListEqual(
            _files_in_dir("/tmp/export",
                          ['proj stem2.wav', 'proj stem4.wav', 'proj stem1.wav', 'proj stem3.wav']),
            stems)

    @patch("os.walk")
    def test_discover_audiofiles_returns_only_related_audio_files(self, walk_mock):
        walk_mock.return_value = _create_walk_files([
            'proj stem2.wav', 'ignore.txt', 'proj stem1.wav', 'proj.wav', 'archive.zip',
            "proj unrelated.mp3"
        ])

        trackpacker = TrackPacker("proj", "/tmp/export")
        (_, stems) = trackpacker.discover_audiofiles()
        self.assertListEqual(_files_in_dir("/tmp/export/", ['proj stem2.wav', 'proj stem1.wav']),
                             stems)

    @patch("os.walk")
    def test_discover_audiofiles_master_track_matches_project_name(self, walk_mock):
        walk_mock.return_value = _create_walk_files(
            ['example.wav', 'proj stem4.wav', 'proj stem1.wav', 'proj.wav', 'proj stem3.wav'])
        trackpacker = TrackPacker("example", "/tmp/export")
        (master, _) = trackpacker.discover_audiofiles()
        self.assertEqual('example.wav', master)

    @patch("os.walk")
    def test_discover_audiofiles_fails_if_no_master(self, walk_mock):
        walk_mock.return_value = _create_walk_files(['proj stem1.wav', 'proj stem2.wav'])

        with self.assertRaises(MissingFileException):
            trackpacker = TrackPacker("proj", "/tmp/export")
            trackpacker.discover_audiofiles()

    @patch("os.walk")
    def test_discover_audiofiles_fails_if_no_stems(self, walk_mock):
        walk_mock.return_value = _create_walk_files(["proj.wav"])

        with self.assertRaises(MissingFileException):
            trackpacker = TrackPacker("proj", "/tmp/export")
            trackpacker.discover_audiofiles()

    @patch("os.walk")
    def test_discover_audiofiles_returns_explicit_passed_audio_files(self, walk_mock):
        walk_mock.return_value = _create_walk_files(
            ['proj stem2.wav', 'proj stem4.wav', 'proj stem1.wav', 'proj.wav', 'proj stem3.wav'])

        trackpacker = TrackPacker("proj", "/tmp/export")
        (master, stems) = trackpacker.discover_audiofiles(
            _files_in_dir("/tmp/export", ["/tmp/x/proj stem1.wav", "/tmp/x/proj stem3.wav"]))
        walk_mock.assert_called_with('/tmp/export')
        self.assertEqual('proj.wav', master)
        self.assertListEqual(_files_in_dir("/tmp/x/", ['proj stem1.wav', 'proj stem3.wav']), stems)

    @patch("trackpack.trackpacker.ZipFile", autospec=True)
    # pylint: disable=R0201
    def test_pack_files_creates_archive_of_stems(self, zip_mock):
        trackpacker = TrackPacker("projname", "/tmp/proj/Export")
        trackpacker.pack_files("archivename",
                               _files_in_dir("/tmp/proj/Export", ["a.wav", "b.wav", "c.wav"]))
        zip_mock.assert_has_calls(
            _create_zip_mock_calls("archivename", "/tmp/proj/Export", {
                "a.wav": "a.wav",
                "b.wav": "b.wav",
                "c.wav": "c.wav"
            }))

    @patch("trackpack.trackpacker.ZipFile", autospec=True)
    # pylint: disable=R0201
    def test_pack_files_removes_project_name_from_stems(self, zip_mock):
        trackpacker = TrackPacker("proj1", "/tmp/x")
        trackpacker.pack_files("archive1",
                               _files_in_dir("/tmp/x", ["proj1 a.wav", "b.wav", "proj1 c.wav"]))
        zip_mock.assert_has_calls(
            _create_zip_mock_calls("archive1", "/tmp/x", {
                "proj1 a.wav": "a.wav",
                "b.wav": "b.wav",
                "proj1 c.wav": "c.wav"
            }))

    @patch("trackpack.trackpacker.ZipFile", autospec=True)
    # pylint: disable=R0201
    def test_pack_files_replaces_blanks_in_names(self, zip_mock):
        trackpacker = TrackPacker("proj1", "/tmp/st u v w")
        trackpacker.pack_files(
            "archive1",
            _files_in_dir("/tmp/st u v w", ["proj1 a a a.wav", "b 123.wav", "proj1 cd  efg.wav"]))
        zip_mock.assert_has_calls(
            _create_zip_mock_calls(
                "archive1", "/tmp/st u v w", {
                    "proj1 a a a.wav": "a-a-a.wav",
                    "b 123.wav": "b-123.wav",
                    "proj1 cd  efg.wav": "cd--efg.wav"
                }))


def _files_in_dir(dirpath, filenames):
    return [os.path.join(dirpath, file) for file in filenames]


def _create_walk_files(files):
    return iter([('proj_export_dir', [], files)])


def _create_zip_mock_calls(archive_name, proj_export_dir, files):
    call_list = [
        call(os.path.join(proj_export_dir, f"{archive_name}.zip"), "w"),
        call().__enter__()
    ]

    for name, entry in files.items():
        call_list.append(call().__enter__().write(os.path.join(proj_export_dir, name), entry))
    call_list.append(call().__exit__(None, None, None))

    return call_list
