# trackpack - Package audio tracks
#
# Copyright (C) 2020-2026  offa
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

import os
import unittest
from unittest.mock import call, patch
from pathlib import Path

from trackpack.trackpacker import MissingFileException, TrackPacker


class TestTrackPack(unittest.TestCase):
    @patch("os.walk")
    def test_discover_audiofiles_returns_audio_files(self, walk_mock) -> None:
        export_dir = Path("/tmp/export")

        walk_mock.return_value = _create_walk_files(
            [
                "proj stem2.wav",
                "proj stem4.wav",
                "proj stem1.wav",
                "proj.wav",
                "proj stem3.wav",
            ]
        )

        trackpacker = TrackPacker("proj", str(export_dir))
        (master, stems) = trackpacker.discover_audiofiles()
        walk_mock.assert_called_with(str(export_dir))
        self.assertEqual("proj.wav", master)
        self.assertListEqual(
            _files_in_dir(
                export_dir,
                [
                    "proj stem2.wav",
                    "proj stem4.wav",
                    "proj stem1.wav",
                    "proj stem3.wav",
                ],
            ),
            stems,
        )

    @patch("os.walk")
    def test_discover_audiofiles_returns_only_related_audio_files(
        self, walk_mock
    ) -> None:
        export_dir = Path("/tmp/export")
        walk_mock.return_value = _create_walk_files(
            [
                "proj stem2.wav",
                "ignore.txt",
                "proj stem1.wav",
                "proj.wav",
                "archive.zip",
                "proj unrelated.mp3",
            ]
        )

        trackpacker = TrackPacker("proj", str(export_dir))
        (_, stems) = trackpacker.discover_audiofiles()
        self.assertListEqual(
            _files_in_dir(export_dir, ["proj stem2.wav", "proj stem1.wav"]), stems
        )

    @patch("os.walk")
    def test_discover_audiofiles_master_track_matches_project_name(
        self, walk_mock
    ) -> None:
        export_dir = Path("/tmp/export")
        walk_mock.return_value = _create_walk_files(
            [
                "example.wav",
                "proj stem4.wav",
                "proj stem1.wav",
                "proj.wav",
                "proj stem3.wav",
            ]
        )
        trackpacker = TrackPacker("example", str(export_dir))
        (master, _) = trackpacker.discover_audiofiles()
        self.assertEqual("example.wav", master)

    @patch("os.walk")
    def test_discover_audiofiles_fails_if_no_master(self, walk_mock) -> None:
        export_dir = Path("/tmp/export")
        walk_mock.return_value = _create_walk_files(
            ["proj stem1.wav", "proj stem2.wav"]
        )

        with self.assertRaises(MissingFileException):
            trackpacker = TrackPacker("proj", str(export_dir))
            trackpacker.discover_audiofiles()

    @patch("os.walk")
    def test_discover_audiofiles_fails_if_no_stems(self, walk_mock) -> None:
        export_dir = Path("/tmp/export")
        walk_mock.return_value = _create_walk_files(["proj.wav"])

        with self.assertRaises(MissingFileException):
            trackpacker = TrackPacker("proj", str(export_dir))
            trackpacker.discover_audiofiles()

    @patch("os.walk")
    def test_discover_audiofiles_returns_explicit_passed_audio_files(
        self, walk_mock
    ) -> None:
        export_dir = Path("/tmp/export")
        temp_dir = Path("/tmp/x")

        walk_mock.return_value = _create_walk_files(
            [
                "proj stem2.wav",
                "proj stem4.wav",
                "proj stem1.wav",
                "proj.wav",
                "proj stem3.wav",
            ]
        )

        trackpacker = TrackPacker("proj", str(export_dir))

        explicit_files_list = ["/tmp/x/proj stem1.wav", "/tmp/x/proj stem3.wav"]

        (master, stems) = trackpacker.discover_audiofiles(explicit_files_list)
        walk_mock.assert_called_with(str(export_dir))
        self.assertEqual("proj.wav", master)
        self.assertListEqual(
            _files_in_dir(temp_dir, ["proj stem1.wav", "proj stem3.wav"]), stems
        )

    @patch("trackpack.trackpacker.ZipFile", autospec=True)
    def test_pack_files_creates_archive_of_stems(self, zip_mock) -> None:
        export_dir = Path("/tmp/proj/Export")
        trackpacker = TrackPacker("projname", str(export_dir))

        files_to_pack = _files_in_dir(export_dir, ["a.wav", "b.wav", "c.wav"])

        trackpacker.pack_files(
            "archivename",
            files_to_pack,
        )
        zip_mock.assert_has_calls(
            _create_zip_mock_calls(
                "archivename",
                str(export_dir),
                {"a.wav": "a.wav", "b.wav": "b.wav", "c.wav": "c.wav"},
            )
        )

    @patch("trackpack.trackpacker.ZipFile", autospec=True)
    def test_pack_files_removes_project_name_from_stems(self, zip_mock) -> None:
        export_dir = Path("/tmp/x")
        trackpacker = TrackPacker("proj1", str(export_dir))

        files_to_pack = _files_in_dir(
            export_dir, ["proj1 a.wav", "b.wav", "proj1 c.wav"]
        )

        trackpacker.pack_files("archive1", files_to_pack)
        zip_mock.assert_has_calls(
            _create_zip_mock_calls(
                "archive1",
                str(export_dir),
                {"proj1 a.wav": "a.wav", "b.wav": "b.wav", "proj1 c.wav": "c.wav"},
            )
        )

    @patch("trackpack.trackpacker.ZipFile", autospec=True)
    def test_pack_files_replaces_blanks_in_names(self, zip_mock) -> None:
        export_dir = Path("/tmp/st u v w")
        trackpacker = TrackPacker("proj1", str(export_dir))

        files_to_pack = _files_in_dir(
            export_dir, ["proj1 a a a.wav", "b 123.wav", "proj1 cd  efg.wav"]
        )

        trackpacker.pack_files("archive1", files_to_pack)
        zip_mock.assert_has_calls(
            _create_zip_mock_calls(
                "archive1",
                str(export_dir),
                {
                    "proj1 a a a.wav": "a-a-a.wav",
                    "b 123.wav": "b-123.wav",
                    "proj1 cd  efg.wav": "cd--efg.wav",
                },
            )
        )


def _files_in_dir(dirpath: Path, filenames: list[str]) -> list[Path]:
    return [Path(dirpath) / file for file in filenames]


def _create_walk_files(files: list[str]):
    return iter([("proj_export_dir", [], files)])


def _create_zip_mock_calls(
    archive_name: str, proj_export_dir: str, files: dict[str, str]
):
    proj_export_dir_path = Path(proj_export_dir)

    call_list = [
        call(proj_export_dir_path / f"{archive_name}.zip", "w"),
        call().__enter__(),  # pylint: disable=unnecessary-dunder-call
    ]

    for name, entry in files.items():
        file_path = proj_export_dir_path / name
        # pylint: disable=unnecessary-dunder-call
        call_list.append(call().__enter__().write(file_path, entry))
    call_list.append(call().__exit__(None, None, None))
    return call_list
