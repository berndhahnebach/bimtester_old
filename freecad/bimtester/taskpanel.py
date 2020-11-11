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

from PySide import QtCore
from PySide import QtGui

import FreeCADGui


"""
from freecad.bimtester import tools_bimtester as tbt
import importlib
importlib.reload(tbt)
tbt.show_panel()

"""


def show_panel():
    QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
    mw = FreeCADGui.getMainWindow()
    awidget = QtGui.QDockWidget("TaskPanelBimTester", mw)
    awidget.setWidget(TaskPanelBimTester())
    mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, awidget)
    QtGui.QApplication.restoreOverrideCursor()


class TaskPanelBimTester(QtGui.QWidget):
    def __init__(self):
        super(TaskPanelBimTester, self).__init__()
        self.init_ui()

    def __del__(self,):
        # need as fix for qt event error
        # http://forum.freecadweb.org/viewtopic.php?f=18&t=10732&start=10#p86493
        return

    def init_ui(self):

        # init widgets
        ui = FreeCADGui.UiLoader()

        self.ifcfile_label = QtGui.QLabel("IFC file", self)
        self.ifcfile_chooser = ui.createWidget("Gui::PrefFileChooser")
        self.ifcfile_chooser.setParent(self)

        ffifc_str = "Feature files beside IFC file"
        self.featuredirfromifc_label = QtGui.QLabel(ffifc_str, self)
        self.featuredirfromifc_checkbox = QtGui.QCheckBox(self)

        ffdir_str = "Feature files directory"
        self.featurefilesdir_label = QtGui.QLabel(ffdir_str, self)
        self.featurefilesdir_chooser = ui.createWidget("Gui::PrefFileChooser")
        self.featurefilesdir_chooser.setParent(self)

        self.buttons = QtGui.QDialogButtonBox(self)
        self.buttons.setOrientation(QtCore.Qt.Horizontal)
        self.setup_button = QtGui.QPushButton(
            QtGui.QIcon.fromTheme("document-new"), "Run"
        )
        self.buttons.addButton(
            self.setup_button, QtGui.QDialogButtonBox.AcceptRole
        )
        self.close_button = QtGui.QPushButton(
            QtGui.QIcon.fromTheme("window-close"), "Close"
        )
        self.buttons.addButton(
            self.close_button, QtGui.QDialogButtonBox.RejectRole
        )
        self.buttons.clicked.connect(self.clicked)

        # Layout:
        layout = QtGui.QGridLayout()
        layout.addWidget(self.ifcfile_label, 1, 0)
        layout.addWidget(self.ifcfile_chooser, 2, 0)
        layout.addWidget(self.featuredirfromifc_label, 3, 0)
        layout.addWidget(self.featuredirfromifc_checkbox, 4, 0)
        layout.addWidget(self.featurefilesdir_label, 5, 0)
        layout.addWidget(self.featurefilesdir_chooser, 6, 0)
        layout.addWidget(self.buttons, 7, 0)
        # row stretches by 10 compared to the others, std is 0
        layout.setRowStretch(0, 10)
        self.setLayout(layout)

    def clicked(self, btn):
        if self.buttons.buttonRole(btn) == QtGui.QDialogButtonBox.AcceptRole:
            self.accept()
        elif self.buttons.buttonRole(btn) == QtGui.QDialogButtonBox.RejectRole:
            self.reject()

    def accept(self):
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        print("accept")

        # get input values
        """
        or_outer_d = int(self.outer_ring_dia_dspin.value())
        if not or_outer_d:
            print("Error in getting or_outer_d.")
            or_outer_d = 129
        """
        print(self.featurefilesdir_chooser.objectName())
        the_features_path = ""
        the_ifcfile_path = ""
        the_ifcfile_name = ""

        # run bimtester
        print("TODO")
        """
        from freecad.bimtester.utils import run_all
        status = run_all(
            the_features_path,
            the_ifcfile_path,
            the_ifcfile_name
        )
        print(status)
        """

        QtGui.QApplication.restoreOverrideCursor()

    def reject(self):
        print("reject")
        self.close()

    def closeEvent(self, ev):
        pw = self.parentWidget()
        if pw and pw.inherits("QDockWidget"):
            pw.deleteLater()
