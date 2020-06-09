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

import argparse

def parse_args(args):
    parser = argparse.ArgumentParser(prog="trackpack", description='Audio tracks packaging')
    subparsers = parser.add_subparsers(dest="command")
    pack_parser = subparsers.add_parser("pack", help="Pack audio files")
    pack_parser.add_argument("pack_explicit_files", metavar="file", nargs="*", help="Files to pack")

    return parser.parse_args(args=args if args else ['--help'])
