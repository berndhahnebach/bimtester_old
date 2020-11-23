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

import steps.helpersmartviewstrings as hss


# this needs to be at the same place
# as the step files and the feature files
# thus if run in separate dir copy this file too


this_path = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(this_path, "..")
sm_file = os.path.join(log_path, "zoombimtestersmartview.bcsv")

def before_all(context):
    userdata = context.config.userdata
    continue_after_failed = True
    Scenario.continue_after_failed_step = continue_after_failed

    """
    # test befora_all ...
    mytestlogfile = open(os.path.join(log_path, "zztest.txt"), "w")
    mytestlogfile.write("myenvironmenttest\n")
    mytestlogfile.write(this_path)
    mytestlogfile.close()
    """

    # set up my log file
    context.thelogfile = os.path.join(log_path, "mybimtesterlog.log")

    # set up smart view file
    context.thesmfile = sm_file
    """
    # since all bimtester tmp is removed first the sm_file
    # does not need to be explicit removed first
    smf = open(sm_file, "w")
    smf.write("{}\n".format(hss.smartviews_string_before))
    smf.close()    
    # TODO
    # create file, write smartviews before
    # in each scenario write the smartview foreach scenario
    # after all here in new method write smartviews after and
    # only one smartview file which consists of lots of smartviews
    """


def after_all(context):

    smf = open(sm_file, "a")
    smf.write("{}\n".format(hss.smartviews_string_after))
    smf.close()    


"""
# https://stackoverflow.com/a/31545036
# https://behave.readthedocs.io/en/latest/tutorial.html#environmental-controls

def before_step(context, step):
    print(step.name)


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
