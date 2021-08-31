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

import sys

from trackpack import cli, config
from trackpack.trackpacker import TrackPacker


def __fail(msg):
    print("ERROR: {}".format(msg))
    sys.exit(1)


def __read_config(filename):
    with open(filename, "r", encoding="utf-8") as config_file:
        cfg = config.Config()
        cfg.load_from_yaml(config_file)
        return cfg


def main():
    args = cli.parse_args(sys.argv[1:])

    if args.command == 'pack':
        try:
            cfg = __read_config("pack.yml")
            cfg.load_from_cli_args(args)

            trackpacker = TrackPacker(cfg.name, cfg.export_dir)
            (_, stems) = trackpacker.discover_audiofiles(args.pack_explicit_files)
            trackpacker.pack_files(cfg.archive_name, stems)
        except FileNotFoundError as ex:
            __fail("{}: {}".format(ex.strerror, ex.filename))


if __name__ == '__main__':
    main()
