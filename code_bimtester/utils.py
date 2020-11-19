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
import platform


def get_logfile_path():

    logfilename = "mybimtesterlog.log"
    if platform.system() == "Windows":
        logfilepath = os.path.join(
            os.path.expanduser('~'),
            'Desktop',
            logfilename
        )
        # logfilepath = "C:/Users/BHA/AppData/Local/Temp/mybimtesterlog.log"
        # logfilepath = "C:/Users/BHA/Desktop/mybimtesterlog.log"
    elif platform.system() == "Linux":
        logfilepath = os.path.join("/", "tmp", logfilename)
    else:
        pass
        # darwin not supported (OSX)
    print(logfilepath)

    return logfilepath


def get_smartview_path():

    smartviewname = "zoomsmartview.bcsv"
    if platform.system() == "Windows":
        smartviewpath = os.path.join(
            os.path.expanduser('~'),
            'Desktop',
            smartviewname
        )
    elif platform.system() == "Linux":
        smartviewpath = os.path.join("/", "tmp", smartviewname)
    else:
        pass
        # darwin not supported (OSX)
    print(smartviewpath)

    return smartviewpath


def create_zoom_smartview(false_elements_guid):

    from .smartviewstrings import smartview_string_before
    from .smartviewstrings import smartview_string_after
    from .smartviewstrings import rule_string_before
    from .smartviewstrings import rule_string_after

    smartviewpath = get_smartview_path()
    smf = open(smartviewpath, "a")
    smf.write("{}\n".format(smartview_string_before))
    for guid in false_elements_guid:
        smf.write("{}{}{}\n".format(rule_string_before, guid, rule_string_after))
    smf.write("{}\n".format(smartview_string_after))
    smf.close()
