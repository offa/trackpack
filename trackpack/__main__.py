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

import yaml
import trackpacker

def __read_config(filename):
    with open(filename, "r") as config_file:
        return yaml.safe_load(config_file)


def main():
    config = __read_config("pack.yml")
    export_dir = "Exports"
    project_name = config["name"]
    archive_name = config.get("archive", project_name)

    (_, stems) = trackpacker.discover_audiofiles(project_name, export_dir)
    trackpacker.pack_files(export_dir, project_name, archive_name, stems)


if __name__ == '__main__':
    main()
