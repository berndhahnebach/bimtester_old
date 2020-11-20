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

import helpersmartviewstrings as hss

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


def get_smartview_path(scenario_name):

    smartviewname = "zoomsmartview_{}.bcsv".format(scenario_name)
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


def create_zoom_smartview(scenario_name, false_elements_guid):

    smartviewpath = get_smartview_path(scenario_name)
    smf = open(smartviewpath, "w")

    # TODO pass all scenarios and features
    scenarios = [scenario_name]

    smf.write("{}\n".format(hss.smartviews_string_before))
    for scenar in scenarios:
        # each_smartview_string_title
        smf.write("            <SMARTVIEW>\n")
        smf.write("                <TITLE>{}, Filter GUID</TITLE>\n".format(scenar))
        smf.write("                <DESCRIPTION></DESCRIPTION>\n")
        smf.write("{}\n".format(hss.each_smartview_string_before))
        for guid in false_elements_guid:
            smf.write(
                "{}{}{}\n".format(
                    hss.rule_string_before,
                    guid,
                    hss.rule_string_after)
            )
        smf.write("{}\n".format(hss.each_smartview_string_after))
    smf.write("{}\n".format(hss.smartviews_string_after))

    smf.close()
