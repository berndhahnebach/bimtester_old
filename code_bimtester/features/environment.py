# ***************************************************************************
# *   Copyright (c) 2020 Dion Moult <>                                      *
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
import os

from behave.model import Scenario


# this needs to be at the same place
# as the step files and the feature files
# thus if run behave in separate dir copy this file too


this_path = os.path.dirname(os.path.realpath(__file__))
out_path = os.path.join(this_path, "..")
# sm_file = os.path.join(out_path, "zoombimtestersmartview.bcsv")


def before_all(context):

    userdata = context.config.userdata
    context.ifcbasename = userdata["ifcbasename"]

    # do not break after a failed scenario
    # https://community.osarch.org/discussion/comment/3328/#Comment_3328
    continue_after_failed = True
    Scenario.continue_after_failed_step = continue_after_failed

    # keep out path
    context.outpath = out_path

    # set up my log file
    context.thelogfile = os.path.join(out_path, "mybimtesterlog.log")

    # set up smart view file
    # since all bimtester tmp is removed first the sm_file
    # does not need to be explicit removed first
    sm_file = os.path.join(out_path, context.ifcbasename + ".bcsv")
    context.thesmfile = sm_file
    smf = open(sm_file, "w")
    smf.write('<?xml version="1.0"?>\n')
    smf.write("<bimcollabsmartviewfile>\n")
    smf.write("    <version>5</version>\n")
    smf.write("    <applicationversion>Win - Version: 3.4 (build 3.4.13.559)</applicationversion>\n")
    smf.write("</bimcollabsmartviewfile>\n")
    smf.write("\n")
    smf.write("<SMARTVIEWSETS>\n")
    smf.write("    <SMARTVIEWSET>\n")
    smf.write("        <TITLE>BIMTester {}</TITLE>\n".format(context.ifcbasename))
    smf.write("        <DESCRIPTION></DESCRIPTION>\n")
    smf.write("        <GUID>a2ddfaf7-97f2-4519-aabd-f2d94f6b4d6b</GUID>\n")
    smf.write("        <MODIFICATIONDATE>2020-10-30T13:23:30</MODIFICATIONDATE>\n")
    smf.write("        <SMARTVIEWS>\n")
    smf.write("        </SMARTVIEWS>\n")
    smf.write("    </SMARTVIEWSET>\n")
    smf.write("</SMARTVIEWSETS>\n")
    smf.close()

    """
    # test before_all ...
    mytestlogfile = open(os.path.join(out_path, "zztest.txt"), "w")
    mytestlogfile.write("myenvironmenttest\n")
    mytestlogfile.write(this_path)
    mytestlogfile.close()
    """


def after_step(context, step):
    if step.status == "failed":
        # take_the_shot(context.scenario.name + " " + step.name)
        print("Step {} failed".format(step.name))
        # works :-) but not after the scenario has finished
        # than out of scope ... thus check for existance
        # we can log an do the smartiew from here only
        if hasattr(context, "falseguids"):
            # print(context.falseguids)

            append_zoom_smartview(
                context.thesmfile,
                context.scenario.name,
                context.falseguids
            )


"""
# https://stackoverflow.com/a/31545036
# https://behave.readthedocs.io/en/latest/tutorial.html#environmental-controls


# the scope of context attriutes set in step is the scenario :-(
# https://behave.readthedocs.io/en/latest/context_attributes.html




# logging the behave way
# https://behave.readthedocs.io/en/latest/api.html#logging-setup
def before_all(context):
    # -- SET LOG LEVEL: behave --logging-level=ERROR ...
    # on behave command-line or in "behave.ini".
    context.config.setup_logging()
"""


def append_zoom_smartview(sm_file, scenario_name, false_elements_guid):

    # build the smartview string
    smview_string = "            <SMARTVIEW>\n"
    smview_string += (
        "                <TITLE>GUID filter, {}</TITLE>\n"
        .format(scenario_name)
    )
    smview_string += "{}\n".format(each_smartview_string_before)
    for guid in false_elements_guid:
        smview_string += (
            "{}{}{}\n".format(
                rule_string_before,
                guid,
                rule_string_after)
        )
    smview_string += "{}\n".format(each_smartview_string_after)

    # insert smartview string into file
    theline = "        </SMARTVIEWS>"
    newtext = smview_string + theline
    for line in fileinput.FileInput(sm_file, inplace=True):
        # the print replaces the line in the file
        # and add the line afterwards
        print(line.replace(theline, newtext), end="")


each_smartview_string_title = """            <SMARTVIEW>
                <TITLE>Filter GUID</TITLE>
                <DESCRIPTION></DESCRIPTION>"""


each_smartview_string_before = """                <CREATOR>bernd@bimstatik.ch</CREATOR>
                <CREATIONDATE>2020-10-30T13:18:45</CREATIONDATE>
                <MODIFIER>bernd@bimstatik.ch</MODIFIER>
                <MODIFICATIONDATE>2020-10-30T13:23:30</MODIFICATIONDATE>
                <GUID>15fda94f-b4bf-43be-8ef4-15d3121137e1</GUID>
                <RULES>
                    <RULE>
                        <IFCTYPE>Any</IFCTYPE>
                        <PROPERTY>
                            <NAME>None</NAME>
                            <PROPERTYSETNAME>None</PROPERTYSETNAME>
                            <TYPE>None</TYPE>
                            <VALUETYPE>None</VALUETYPE>
                            <UNIT>None</UNIT>
                        </PROPERTY>
                        <CONDITION>
                            <TYPE>Is</TYPE>
                            <VALUE></VALUE>
                        </CONDITION>
                        <ACTION>
                            <TYPE>AddSetColored</TYPE>
                            <R>187</R>
                            <G>187</G>
                            <B>187</B>
                        </ACTION>
                    </RULE>
                    <RULE>
                        <IFCTYPE>Any</IFCTYPE>
                        <PROPERTY>
                            <NAME>None</NAME>
                            <PROPERTYSETNAME>None</PROPERTYSETNAME>
                            <TYPE>None</TYPE>
                            <VALUETYPE>None</VALUETYPE>
                            <UNIT>None</UNIT>
                        </PROPERTY>
                        <CONDITION>
                            <TYPE>Is</TYPE>
                            <VALUE></VALUE>
                        </CONDITION>
                        <ACTION>
                            <TYPE>SetTransparent</TYPE>
                        </ACTION>
                    </RULE>"""


each_smartview_string_after = """                </RULES>
                <INFORMATIONTAKEOFF>
                    <PROPERTYSETNAME>None</PROPERTYSETNAME>
                    <PROPERTYNAME>None</PROPERTYNAME>
                    <OPERATION>0</OPERATION>
                </INFORMATIONTAKEOFF>
            </SMARTVIEW>"""


rule_string_before = """                    <RULE>
                        <IFCTYPE>Any</IFCTYPE>
                        <PROPERTY>
                            <NAME>GUID</NAME>
                            <PROPERTYSETNAME>Summary</PROPERTYSETNAME>
                            <TYPE>Summary</TYPE>
                            <VALUETYPE>StringValue</VALUETYPE>
                            <UNIT>None</UNIT>
                        </PROPERTY>
                        <CONDITION>
                            <TYPE>Is</TYPE>
                            <VALUE>"""


rule_string_after = """</VALUE>
                        </CONDITION>
                        <ACTION>
                            <TYPE>SetColored</TYPE>
                            <R>255</R>
                            <G>10</G>
                            <B>10</B>
                        </ACTION>
                    </RULE>"""
