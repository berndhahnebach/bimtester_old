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

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from .fcbimtester import run_all


"""
TODO
if self._featuredirfromifc_cb.isChecked()
 feature path browser und lineedit should be deactivated
"""


class TaskPanelBimTester(QtWidgets.QWidget):

    ifcfile_changed = QtCore.Signal()
    featurefilesdir_changed = QtCore.Signal()

    # get feature files directory path
    # import features_bimtester
    # base_features_path = os.path.split(features_bimtester.__file__)[0]
    base_features_path = "."
    print(base_features_path)

    def __init__(self):
        super(TaskPanelBimTester, self).__init__()
        self._setup_ui()

    def __del__(self,):
        # need as fix for qt event error
        # http://forum.freecadweb.org/viewtopic.php?f=18&t=10732&start=10#p86493
        return

    def _setup_ui(self):

        # init widgets
        # ui = FreeCADGui.UiLoader()

        # https://forum.freecadweb.org/viewtopic.php?f=10&t=51419
        # use a browse button, and a line edit
        # the browse button opens a file dialog, which will set the line edit
        # see solver frame work task panel in FEM

        # icon
        # print(__file__)
        package_path = os.path.dirname(os.path.realpath(__file__))
        iconpath = os.path.join(
            package_path, "resources", "icons", "bimtester.svg"
        )
        """
        # svg
        # https://stackoverflow.com/a/35138314
        theicon = QtSvg.QSvgWidget(iconpath)
        # none works ...
        #theicon.setGeometry(20,20,200,200)
        #theicon.setSizePolicy(QtGui.QSizePolicy.Policy.Maximum, QtGui.QSizePolicy.Policy.Maximum)
        #theicon.sizeHint()
        """
        # pixmap
        theicon = QtWidgets.QLabel(self)
        iconpixmap = QtGui.QPixmap(iconpath)
        iconpixmap = iconpixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
        theicon.setPixmap(iconpixmap)

        # ifc file
        ifcfile_label = QtWidgets.QLabel("IFC file", self)
        self._ifcfile_text = QtWidgets.QLineEdit()
        self._ifcfile_text.editingFinished.connect(self.ifcfile_changed)
        ifcfile_browse_btn = QtWidgets.QToolButton()
        ifcfile_browse_btn.setText("...")
        ifcfile_browse_btn.clicked.connect(self._select_ifcfile)

        # beside button
        ffifc_str = (
            "Feature files beside IFC file. "
            "Feature files in directory features."
        )
        featuredirfromifc_label = QtWidgets.QLabel(ffifc_str, self)
        self._featuredirfromifc_cb = QtWidgets.QCheckBox(self)

        # feature files path
        _ffdir_str = (
            "Feature files directory. "
            "Feature files in directory features."
        )
        featurefilesdir_label = QtWidgets.QLabel(_ffdir_str, self)
        self._featurefilesdir_text = QtWidgets.QLineEdit()
        self.set_featurefilesdir(self.base_features_path)
        self._featurefilesdir_text.editingFinished.connect(
            self.featurefilesdir_changed
        )
        featurefilesdir_browse_btn = QtWidgets.QToolButton()
        featurefilesdir_browse_btn.setText("...")
        featurefilesdir_browse_btn.clicked.connect(
            self._select_featurefilesdir
        )

        # buttons
        self._buttons = QtWidgets.QDialogButtonBox(self)
        self._buttons.setOrientation(QtCore.Qt.Horizontal)
        setup_button = QtWidgets.QPushButton(
            QtGui.QIcon.fromTheme("document-new"), "Run"
        )
        self._buttons.addButton(
            setup_button, QtWidgets.QDialogButtonBox.AcceptRole
        )
        close_button = QtWidgets.QPushButton(
            QtGui.QIcon.fromTheme("window-close"), "Close"
        )
        self._buttons.addButton(
            close_button, QtWidgets.QDialogButtonBox.RejectRole
        )
        self._buttons.clicked.connect(self.clicked)

        # Layout:
        layout = QtWidgets.QGridLayout()
        layout.addWidget(theicon, 1, 0, alignment=QtCore.Qt.AlignRight)
        layout.addWidget(ifcfile_label, 2, 0)
        layout.addWidget(self._ifcfile_text, 3, 0)
        layout.addWidget(ifcfile_browse_btn, 3, 1)
        layout.addWidget(featurefilesdir_label, 4, 0)
        layout.addWidget(self._featurefilesdir_text, 5, 0)
        layout.addWidget(featurefilesdir_browse_btn, 5, 1)
        layout.addWidget(featuredirfromifc_label, 6, 0)
        layout.addWidget(self._featuredirfromifc_cb, 6, 1)
        layout.addWidget(self._buttons, 7, 0)
        # row stretches by 10 compared to the others, std is 0
        # first parameter is the row number
        # second is the stretch factor.
        layout.setRowStretch(0, 10)
        self.setLayout(layout)

    @QtCore.Slot()
    def _select_ifcfile(self):
        # print(self.get_ifcfile())
        # print(os.path.isfile(self.get_ifcfile()))
        ifcfile = QtWidgets.QFileDialog.getOpenFileName(
            self,
            dir="/home/hugo/Documents/zeug_sort/z_some_ifc/3_15025_KiGa_ING_N_TRW.ifc"
            #dir=self.get_ifcfile()
        )[0]
        self.set_ifcfile(ifcfile)
        self.ifcfile_changed.emit()

    @QtCore.Slot(float)
    def set_ifcfile(self, a_file):
        self._ifcfile_text.setText(a_file)

    def get_ifcfile(self):
        return self._ifcfile_text.text()

    @QtCore.Slot()
    def _select_featurefilesdir(self):
        thedir = self._featurefilesdir_text.text()
        # print(thedir)
        # print(os.path.isdir(thedir))
        # hidden directories are only shown if the option is set
        features_path = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            caption="Choose features directory ...",
            dir="/home/hugo/.FreeCAD/Mod/bimtester/features_bimtester/fea_min/",
            #dir=thedir,
            options=QtWidgets.QFileDialog.HideNameFilterDetails
        )
        self.set_featurefilesdir(features_path)
        self.featurefilesdir_changed.emit()

    @QtCore.Slot(float)
    def set_featurefilesdir(self, a_directory):
        self._featurefilesdir_text.setText(a_directory)

    def get_featurefilesdir(self):
        return self._featurefilesdir_text.text()

    # **********************************************************
    def clicked(self, btn):
        if self._buttons.buttonRole(btn) == QtWidgets.QDialogButtonBox.AcceptRole:
            self.accept()
        elif self._buttons.buttonRole(btn) == QtWidgets.QDialogButtonBox.RejectRole:
            self.reject()

    def accept(self):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
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
        # from code_bimtester.fcbimtester import run_all
        status = run_all(
            the_features_path,
            the_ifcfile_path,
            the_ifcfile_name
        )
        print(status)

        QtWidgets.QApplication.restoreOverrideCursor()

    def reject(self):
        print("reject")
        self.close()

    def closeEvent(self, ev):
        pw = self.parentWidget()
        if pw and pw.inherits("QDockWidget"):
            pw.deleteLater()
