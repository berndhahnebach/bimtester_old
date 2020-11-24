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

    # do not bread after a failed scenario
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


"""
# https://stackoverflow.com/a/31545036
# https://behave.readthedocs.io/en/latest/tutorial.html#environmental-controls


# the scope of context attriutes set in step is the scenario :-(
# https://behave.readthedocs.io/en/latest/context_attributes.html


def after_step(context, step):
    if step.status == "failed":
        # take_the_shot(context.scenario.name + " " + step.name)
        print("BERND")


# logging the behave way
# https://behave.readthedocs.io/en/latest/api.html#logging-setup
def before_all(context):
    # -- SET LOG LEVEL: behave --logging-level=ERROR ...
    # on behave command-line or in "behave.ini".
    context.config.setup_logging()
"""
