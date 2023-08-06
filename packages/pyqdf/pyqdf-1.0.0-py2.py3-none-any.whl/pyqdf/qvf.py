# ***** BEGIN GPL LICENSE BLOCK *****
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#   The Original Code is Copyright (C) 2019, Paralelo Consultoria e Servicos Ltda
#   All rights reserved.
# ***** END GPL LICENSE BLOCK *****

import os

class Qvf():

    def __init__(self, qvf='', path=os.getcwd()):
        self.qvf_path = path
        self.qvf_name = qvf
        self.qvf_size_mb = os.path.getsize(self.qvf_path + self.qvf_name) / 1000000

    