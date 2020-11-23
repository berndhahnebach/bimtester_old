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

import fileinput

import helpersmartviewstrings as hss


# try to add the method to context in environment
# this module would be not needed anymore


def append_zoom_smartview(sm_file, scenario_name, false_elements_guid):

    # build the smartview string
    smview_string = "            <SMARTVIEW>\n"
    smview_string += (
        "                <TITLE>GUID filter, {}</TITLE>\n"
        .format(scenario_name)
    )
    smview_string += "{}\n".format(hss.each_smartview_string_before)
    for guid in false_elements_guid:
        smview_string += (
            "{}{}{}\n".format(
                hss.rule_string_before,
                guid,
                hss.rule_string_after)
        )
    smview_string += "{}\n".format(hss.each_smartview_string_after)

    # insert smartview string into file
    theline = "        </SMARTVIEWS>"
    newtext = smview_string + theline
    for line in fileinput.FileInput(sm_file, inplace=True):
        # the print replaces the line in the file
        # and add the line afterwards
        print(line.replace(theline, newtext), end="")
