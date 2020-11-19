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

# TODO merge into bimtester and make a PR to official bimtester module

import fileinput
import os
import shutil
import tempfile

# import FreeCAD

# get bimtester source code module path
bimtester_path = os.path.dirname(os.path.realpath(__file__))
# print(bimtester_path)


"""
# TODO add example code to use run_all method

from freecad.bimtester import fcbimtester
myfeatures_path = "/home/hugo/Desktop/zeug/SEER_FC/"
myfeatures_path = "/home/hugo/Desktop/zeug/ifcos_bimtester/bimtester/myrun"
myifcfile_path = myfeatures_path
runpath = fcbimtester.run_intmp_tests({"features": myfeatures_path, "ifcpath": myifcfile_path})
fcbimtester.generate_report(runpath)

from code_bimtester import fcbimtester
myfeatures_path = "/home/hugo/.FreeCAD/Mod/bimtester/features_bimtester/"
myifcfile_path = "/home/hugo/Documents/zeug_sort/z_some_ifc/"
ifcfilename = "3_15025_KiGa_ING_N_TRW.ifc"
runpath = fcbimtester.run_intmp_tests({"features": myfeatures_path, "ifcpath": myifcfile_path, "ifcfilename": ifcfilename})
fcbimtester.generate_report(runpath)

"""

"""
# clean logs to be able to run tests
# once again but on another building model and in another directory
# somehow does not work, thus test will be rund in the same directory
# directory will be deleted before each new run
# https://github.com/behave/behave/issues/871
# run bimtester
# copy manually this code, run code again, does not work
from behave.runner_util import reset_runtime
reset_runtime()

"""


def run_intmp_tests(args={}):

    from behave import __version__ as behave_version
    # https://github.com/behave/behave/issues/871
    if behave_version == "1.2.5":
        print(
            "At least behave version 1.2.6 is needed, but version {} found."
            .format(behave_version)
        )
        return False

    # mandatory parameter: ifcdir, featuredir
    # optional parameter: ifcfilename
    # copy features and steps to tmp, replace ifcdir in features files
    # run

    # get ifcpath, this is the path the ifc file is in
    if "ifcpath" in args and args["ifcpath"] != "":
        # TODO check if path exists
        ifc_path = args["ifcpath"]
    else:
        print("No ifc path was given.")
        return False

    # get the features_path, the feature files where the tests are in
    if "features" in args and args["features"] != "":
        # TODO check if path exists, and if features dir is inside
        features_path = os.path.join(args["features"], "features")
    else:
        print("No features path was given.")
        return False

    if "ifcfilename" in args and args["ifcfilename"] != "":
        # TODO check if file
        ifc_filename = args["ifcfilename"]
    else:
        ifc_filename = None

    # set up paths
    # a unique temp path should not be used
    # behave raises an ambiguous step exception
    # run_path = tempfile.mkdtemp()
    # thus use the same path on every run
    # but delete it if exists
    run_path = os.path.join(tempfile.gettempdir(), "bimtesterfc")
    if os.path.isdir(run_path):
        from shutil import rmtree
        rmtree(run_path)  # fails on read only files
    if os.path.isdir(run_path):
        print("Delete former beimtester run dir {} failed".format(run_path))
        return False
    os.mkdir(run_path)
    report_path = os.path.join(run_path, "report")
    copy_features_path = os.path.join(run_path, "features")
    copy_steps_path = os.path.join(copy_features_path, "steps")

    # copy features files
    # print(features_path)
    # print(copy_features_path)
    if os.path.exists(features_path):
        shutil.copytree(features_path, copy_features_path)

    # replace ifcpath in feature files
    # IMHO better than copy the ifc file which could be 500 MB
    feature_files = os.listdir(copy_features_path)
    # print(feature_files)
    for feature_file in feature_files:
        feature_file = os.path.join(copy_features_path, feature_file)
        # print(feature_file)
        # search the line
        ff = open(feature_file, "r")
        lines = ff.readlines()
        ff.close()
        theline = ""
        for line in lines:
            if "* The IFC file" in line and "must be provided" in line:
                theline = line
                if ifc_filename is None:
                    ifc_filename = os.path.basename(theline.split('"')[1])
                newifcline = (
                    ' * The IFC file "{}" must be provided\n'
                    .format(os.path.join(ifc_path, ifc_filename))
                )
                # print(newifcline)
                break
        else:
            print("The line which sets the ifc file to test was not found.")
            newifcline = ""
        # replace the line
        if newifcline != "":
            # https://stackoverflow.com/a/290494
            for line in fileinput.input(feature_file, inplace=True):
                # the print replaces the line in the file
                print(line.replace(theline, newifcline), end="")

    # copy step files
    steps_path = os.path.join(bimtester_path,  "features", "steps")
    # print(steps_path)
    # print(copy_steps_path)
    if os.path.exists(steps_path):
        shutil.copytree(steps_path, copy_steps_path)

    # get advanced args
    # print to console from inside step files, add "--no-capture" flag
    # https://github.com/behave/behave/issues/346
    behave_args = [copy_features_path]
    if "advanced_arguments" in args:
        behave_args.extend(args["advanced_arguments"].split())
    elif "console" not in args:
        behave_args.extend([
            "--no-capture",
            "--format",
            "json.pretty",
            "--outfile",
            os.path.join(report_path, "report.json")
        ])
    print(behave_args)

    # run tests
    from behave.__main__ import main as behave_main
    behave_main(behave_args)
    print("All tests are finished.")

    # delete steps
    # shutil.rmtree(steps_path)

    return run_path


def generate_report(adir=None):
    from .bimtester import generate_report
    if adir is None:
        generate_report()
    else:
        generate_report(adir)


def run_all(the_features_path, the_ifcfile_path, the_ifcfile_name):

    # feature files
    feature_files = os.listdir(
        os.path.join(the_features_path, "features")
    )
    print(feature_files)

    # setup log
    #from .utilsbimtester import get_logfile_path
    #logfile = open(get_logfile_path(), "w")
    #logfile.write("BimTester log file\n\n")
    #logfile.close()

    # run bimtester
    runpath = run_intmp_tests({
        "features": the_features_path,
        "ifcpath": the_ifcfile_path,
        "ifcfilename": the_ifcfile_name
    })

    # create html report
    generate_report(runpath)
    print(runpath)

    # open the webbrowser, shoul be separated as well
    import webbrowser
    for ff in feature_files:
        webbrowser.open(os.path.join(
            runpath,
            "report",
            ff + ".html"
        ))

    return True
