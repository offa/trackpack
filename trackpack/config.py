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
from datetime import date


class Config:

    def __init__(self):
        self.name = "unnamed"
        self._archive_name = "unnamed"
        self.export_dir = "Export"
        self.append_date = False

    @property
    def archive_name(self):
        if self.append_date:
            return "-".join((self._archive_name, date.today().strftime('%Y-%m-%d')))
        return self._archive_name

    @archive_name.setter
    def archive_name(self, archive_name):
        if archive_name.endswith(".zip"):
            self._archive_name = archive_name[:-4]
        else:
            self._archive_name = archive_name

    def load_from_yaml(self, yaml_content):
        config = yaml.safe_load(yaml_content)
        self.name = config["name"]
        self.archive_name = config.get("archive", self.name)
        self.append_date = config.get("append_date", False)
