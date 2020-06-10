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

import sys
from datetime import date
import yaml
from trackpack import cli
from trackpack import trackpacker


def __read_config(filename):
    with open(filename, "r") as config_file:
        return yaml.safe_load(config_file)


def main():
    args = cli.parse_args(sys.argv[1:])

    if args.command == 'pack':
        config = __read_config("pack.yml")
        export_dir = "Exports"
        project_name = config["name"]
        archive_name = config.get("archive", project_name)

        if args.archive_name:
            archive_name = args.archive_name

        if args.archive_name.endswith(".zip"):
            archive_name = args.archive_name[:-4]

        if config.get("append_date", False):
            archive_name = "-".join((archive_name, date.today().strftime('%Y-%m-%d')))

        (_, stems) = trackpacker.discover_audiofiles(project_name, export_dir,
                                                     args.pack_explicit_files)
        trackpacker.pack_files(export_dir, project_name, archive_name, stems)


if __name__ == '__main__':
    main()
