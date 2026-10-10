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
from pathlib import Path
from zipfile import ZipFile


class MissingFileException(Exception):
    pass


class TrackPacker:
    def __init__(self, project_name: str, export_dir: str) -> None:
        self._project_name = project_name
        self._export_dir = Path(export_dir)

    def discover_audiofiles(self, explicit_files: list[str] | None = None):
        filenames = [f for _, _, files in os.walk(str(self._export_dir)) for f in files]

        master = f"{self._project_name}.wav"
        files = [f for f in filenames if f.endswith(".wav")]

        if master not in files:
            raise MissingFileException("Master track not found")
        files.remove(master)

        if explicit_files:
            files = [Path(file).resolve() for file in explicit_files]
        else:
            files = [self._export_dir / f for f in files]

        if not files:
            raise MissingFileException("No stems found")

        return (master, [f.resolve() for f in files])

    def pack_files(self, archive_name: str, files: list[Path]):
        archive_path = self._export_dir / f"{archive_name}.zip"
        with ZipFile(archive_path, "w") as archive:
            for file in files:
                archive.write(file, self._normalize_stem_name(file.name))

    def _normalize_stem_name(self, stem_name: str) -> str:
        stem_name = stem_name.removeprefix(self._project_name)
        return stem_name.strip().replace(" ", "-")
