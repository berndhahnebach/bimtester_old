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


"""
from freecad.bimtester import task_panel as tp
import importlib
importlib.reload(tp)
tp.show_panel()

TODO
wenn self._featuredirfromifc_cb.isChecked()
dann sollte featur path browser und lineedit inaktiv sein
"""


def show_panel():
    QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
    mw = FreeCADGui.getMainWindow()
    awidget = QtGui.QDockWidget("TaskPanelBimTester", mw)
    awidget.setWidget(TaskPanelBimTester())
    mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, awidget)
    QtGui.QApplication.restoreOverrideCursor()


class TaskPanelBimTester(QtGui.QWidget):

    ifcfile_changed = QtCore.Signal()
    featurefilesdir_changed = QtCore.Signal()

    def __init__(self):
        super(TaskPanelBimTester, self).__init__()
        self._setup_ui()

    def __del__(self,):
        # need as fix for qt event error
        # http://forum.freecadweb.org/viewtopic.php?f=18&t=10732&start=10#p86493
        return

    def _setup_ui(self):

        # init widgets
        ui = FreeCADGui.UiLoader()

        # https://forum.freecadweb.org/viewtopic.php?f=10&t=51419
        # use a browse button, and a line edit
        # the browse button opens a file dialog, which will set the line edit
        # see solver frame work task panel in FEM

        # ifc file
        ifcfile_label = QtGui.QLabel("IFC file", self)
        self._ifcfile_text = QtGui.QLineEdit()
        self._ifcfile_text.editingFinished.connect(self.ifcfile_changed)
        ifcfile_browse_btn = QtGui.QToolButton()
        ifcfile_browse_btn.setText("...")
        ifcfile_browse_btn.clicked.connect(self._select_ifcfile)

        # beside button
        ffifc_str = "Feature files beside IFC file"
        featuredirfromifc_label = QtGui.QLabel(ffifc_str, self)
        self._featuredirfromifc_cb = QtGui.QCheckBox(self)

        # feature files path
        _ffdir_str = "Feature files directory"
        featurefilesdir_label = QtGui.QLabel(_ffdir_str, self)
        self._featurefilesdir_text = QtGui.QLineEdit()
        self._featurefilesdir_text.editingFinished.connect(self.featurefilesdir_changed)
        featurefilesdir_browse_btn = QtGui.QToolButton()
        featurefilesdir_browse_btn.setText("...")
        featurefilesdir_browse_btn.clicked.connect(self._select_featurefilesdir)

        # buttons
        self._buttons = QtGui.QDialogButtonBox(self)
        self._buttons.setOrientation(QtCore.Qt.Horizontal)
        setup_button = QtGui.QPushButton(
            QtGui.QIcon.fromTheme("document-new"), "Run"
        )
        self._buttons.addButton(
            setup_button, QtGui.QDialogButtonBox.AcceptRole
        )
        close_button = QtGui.QPushButton(
            QtGui.QIcon.fromTheme("window-close"), "Close"
        )
        self._buttons.addButton(
            close_button, QtGui.QDialogButtonBox.RejectRole
        )
        self._buttons.clicked.connect(self.clicked)

        # Layout:
        layout = QtGui.QGridLayout()
        layout.addWidget(ifcfile_label, 1, 0)
        layout.addWidget(self._ifcfile_text, 2, 0)
        layout.addWidget(ifcfile_browse_btn, 2, 1)
        layout.addWidget(featuredirfromifc_label, 3, 0)
        layout.addWidget(self._featuredirfromifc_cb, 4, 0)
        layout.addWidget(featurefilesdir_label, 5, 0)
        layout.addWidget(self._featurefilesdir_text, 6, 0)
        layout.addWidget(featurefilesdir_browse_btn, 6, 1)
        layout.addWidget(self._buttons, 7, 0)
        # row stretches by 10 compared to the others, std is 0
        layout.setRowStretch(0, 10)
        self.setLayout(layout)

    @QtCore.Slot()
    def _select_ifcfile(self):
        ifcfile = QtGui.QFileDialog.getOpenFileName(self)[0]
        self.set_ifcfile(ifcfile)
        self.ifcfile_changed.emit()

    @QtCore.Slot(float)
    def set_ifcfile(self, a_file):
        self._ifcfile_text.setText(a_file)

    def get_ifcfile(self):
        return self._ifcfile_text.text()

    @QtCore.Slot()
    def _select_featurefilesdir(self):
        path = QtGui.QFileDialog.getExistingDirectory(self)
        self.set_featurefilesdir(path)
        self.featurefilesdir_changed.emit()

    @QtCore.Slot(float)
    def set_featurefilesdir(self, a_directory):
        self._featurefilesdir_text.setText(a_directory)

    def get_featurefilesdir(self):
        return self._featurefilesdir_text.text()

    # **********************************************************
    def clicked(self, btn):
        if self._buttons.buttonRole(btn) == QtGui.QDialogButtonBox.AcceptRole:
            self.accept()
        elif self._buttons.buttonRole(btn) == QtGui.QDialogButtonBox.RejectRole:
            self.reject()

    def accept(self):
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        print("accept")

        # get input values
        splitifcpath = os.path.split(self.get_ifcfile())
        the_ifcfile_path, the_ifcfile_name = splitifcpath[0], splitifcpath[1]
        if self._featuredirfromifc_cb.isChecked() is True:
            the_features_path = the_ifcfile_path
            print(
                "Fatur files should be beside ifc "
                "in a directory named 'features'."
            )
        else:
            the_features_path = self.get_featurefilesdir()

        print(the_features_path)
        print(the_ifcfile_path)
        print(the_ifcfile_name)

        # run bimtester
        print("start bimtester")
        from freecad.bimtester.utils import run_all
        status = run_all(
            the_features_path,
            the_ifcfile_path,
            the_ifcfile_name
        )
        print(status)

        QtGui.QApplication.restoreOverrideCursor()

    def reject(self):
        print("reject")
        self.close()

    def closeEvent(self, ev):
        pw = self.parentWidget()
        if pw and pw.inherits("QDockWidget"):
            pw.deleteLater()
