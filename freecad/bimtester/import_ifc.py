# ***************************************************************************
# *   Copyright (c) 2020 Bernd Hahnebach <bernd@bimstatik.org>              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

import os

# import FreeCAD


if open.__module__ == "io":
    # because we'll redefine open below
    pyopen = open


def open(filename):

    # ifc file
    # print(filename)
    splitpath = os.path.split(filename)
    the_ifcfile_path, the_ifcfile_name = splitpath[0], splitpath[1]

    # feature files path
    import features_bimtester
    the_features_path = os.path.split(features_bimtester.__file__)[0]

    print(the_features_path)
    print(the_ifcfile_path)
    print(the_ifcfile_name)

    from code_bimtester.fcbimtester import run_all
    status = run_all(
        the_features_path,
        the_ifcfile_path,
        the_ifcfile_name
    )

    return status
