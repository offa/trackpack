# trackpack - Package audio tracks
#
# Copyright (C) 2020-2022  offa
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
from zipfile import ZipFile


class MissingFileException(Exception):
    pass


class TrackPacker:

    def __init__(self, project_name, export_dir):
        self.__project_name = project_name
        self.__export_dir = export_dir

    def discover_audiofiles(self, explicit_files=None):
        (_, _, filenames) = next(os.walk(self.__export_dir))
        master = f"{self.__project_name}.wav"
        files = list(filter(lambda f: f.endswith(".wav"), filenames))

        if master not in files:
            raise MissingFileException("Master track not found")
        files.remove(master)

        if explicit_files:
            files = [os.path.abspath(file) for file in explicit_files]
        else:
            files = [os.path.abspath(os.path.join(self.__export_dir, file)) for file in files]

        if not files:
            raise MissingFileException("No stems found")

        return (master, [os.path.abspath(file) for file in files])

    def pack_files(self, archive_name, files):
        with ZipFile(f"{os.path.join(self.__export_dir, archive_name)}.zip", "w") as archive:
            for file in files:
                archive.write(file, self.__normalize_stem_name(os.path.basename(file)))

    def __normalize_stem_name(self, stem_name):
        if stem_name.startswith(self.__project_name):
            stem_name = stem_name[len(self.__project_name):]
        return stem_name.strip().replace(" ", "-")
