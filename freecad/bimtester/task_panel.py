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

from PySide import QtCore
from PySide import QtGui

import FreeCADGui

from code_bimtester.bimtester.guiwidget import GuiWidgetBimTester as TaskPanel


"""
from freecad.bimtester import task_panel as tp
tp.show_panel()

"""


# TODO read features and ifcfile in FreeCAD from user pref


def show_panel():
    from bimtesterdata_features import package_path
    init_panel(
        os.path.join(package_path, "fea_min"),
        # "C:/Users/BHA/Desktop/geomtest/Wand_Decke.ifc",
        "/home/hugo/Documents/zeug_sort/z_some_ifc/example_model.ifc"
    )


def init_panel(features="", ifcfile=""):
    QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
    mw = FreeCADGui.getMainWindow()
    awidget = QtGui.QDockWidget("BimTesterGui", mw)
    awidget.setWidget(TaskPanel(features, ifcfile))
    mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, awidget)
    QtGui.QApplication.restoreOverrideCursor()
