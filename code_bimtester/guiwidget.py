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

# TODO: improve layout, start with feature file path and beside button !!!!!
# TODO: if browse widgets will be canceled, last QLineEdit should be restored

import os

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from .fcbimtester import run_all


class GuiWidgetBimTester(QtWidgets.QWidget):

    print(__file__)
    # get some initial values
    initial_ifcfile = "/home/hugo/Documents/zeug_sort/z_some_ifc/3_15025_KiGa_ING_N_TRW.ifc"
    # import features_bimtester
    # initial_featurespath = os.path.split(features_bimtester.__file__)[0]
    # initial_featurespath = "."
    initial_featurespath = "/home/hugo/.FreeCAD/Mod/bimtester/features_bimtester/fea_min"

    def __init__(self):
        super(GuiWidgetBimTester, self).__init__()
        self._setup_ui()

    def __del__(self,):
        # need as fix for qt event error
        # http://forum.freecadweb.org/viewtopic.php?f=18&t=10732&start=10#p86493
        return

    def _setup_ui(self):

        # a lot code is taken from FreeCAD FEM solver frame work task panel
        # https://forum.freecadweb.org/viewtopic.php?f=10&t=51419
        # use a browse button, and a line edit
        # the browse button opens a file dialog, which will set the line edit

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
        self.set_ifcfile(self.initial_ifcfile)
        ifcfile_browse_btn = QtWidgets.QToolButton()
        ifcfile_browse_btn.setText("...")
        ifcfile_browse_btn.clicked.connect(self._select_ifcfile)

        # feature files path
        # use a layout with a frame and a title, see solver framework tp
        # beside button
        ffifc_str = (
            "Feature files beside IFC file. "
            "Feature files in directory features."
        )
        featuredirfromifc_label = QtWidgets.QLabel(ffifc_str, self)
        self._featuredirfromifc_cb = QtWidgets.QCheckBox(self)
        self._featuredirfromifc_cb.stateChanged.connect(self.mybeside)

        # path browser and line edit
        _ffdir_str = (
            "Feature files directory. "
            "Feature files in directory features."
        )
        featurefilesdir_label = QtWidgets.QLabel(_ffdir_str, self)
        self._featurefilesdir_text = QtWidgets.QLineEdit()
        self.set_featurefilesdir(self.initial_featurespath)
        featurefilesdir_browse_btn = QtWidgets.QToolButton()
        featurefilesdir_browse_btn.setText("...")
        featurefilesdir_browse_btn.clicked.connect(
            self._select_featurefilesdir
        )

        # buttons
        self._run_button = QtWidgets.QPushButton(
            QtGui.QIcon.fromTheme("document-new"), "Run"
        )
        self._close_button = QtWidgets.QPushButton(
            QtGui.QIcon.fromTheme("window-close"), "Close"
        )
        self._run_button.clicked.connect(self.run_bimtester)
        self._close_button.clicked.connect(self.close_widget)
        _buttons = QtWidgets.QHBoxLayout()
        _buttons.addWidget(self._run_button)
        _buttons.addWidget(self._close_button)

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
        layout.addLayout(_buttons, 7, 0)
        # row stretches by 10 compared to the others, std is 0
        # first parameter is the row number
        # second is the stretch factor.
        layout.setRowStretch(0, 10)
        self.setLayout(layout)

    # **********************************************************
    def _select_ifcfile(self):
        # print(self.get_ifcfile())
        # print(os.path.isfile(self.get_ifcfile()))
        ifcfile = QtWidgets.QFileDialog.getOpenFileName(
            self,
            dir=self.get_ifcfile()
        )[0]
        self.set_ifcfile(ifcfile)

    def set_ifcfile(self, a_file):
        self._ifcfile_text.setText(a_file)

    def get_ifcfile(self):
        return self._ifcfile_text.text()

    def mybeside(self):
        print("TODO...TODO")
        # TODO
        # rename method
        # deactivate feature path browser button
        # delete lineedit text
        # deactivate lineedit text

    def _select_featurefilesdir(self):
        thedir = self._featurefilesdir_text.text()
        # print(thedir)
        # print(os.path.isdir(thedir))
        # hidden directories are only shown if the option is set
        features_path = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            caption="Choose features directory ...",
            dir=thedir,
            options=QtWidgets.QFileDialog.HideNameFilterDetails
        )
        self.set_featurefilesdir(features_path)

    def set_featurefilesdir(self, a_directory):
        self._featurefilesdir_text.setText(a_directory)

    def get_featurefilesdir(self):
        return self._featurefilesdir_text.text()

    # **********************************************************
    def run_bimtester(self):
        print("Run BIMTester")
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        # get input values
        splitifcpath = os.path.split(self.get_ifcfile())
        the_ifcfile_path, the_ifcfile_name = splitifcpath[0], splitifcpath[1]
        if self._featuredirfromifc_cb.isChecked() is True:
            the_features_path = the_ifcfile_path
            print(
                "Make sure the feature files are beside "
                "the ifc file in a directory named 'features'."
            )
        else:
            the_features_path = self.get_featurefilesdir()
        print(the_features_path)
        print(the_ifcfile_path)
        print(the_ifcfile_name)

        # run bimtester
        # from code_bimtester.fcbimtester import run_all
        status = run_all(
            the_features_path,
            the_ifcfile_path,
            the_ifcfile_name
        )
        print(status)

        QtWidgets.QApplication.restoreOverrideCursor()

    def close_widget(self):
        print("Close BIMTester Gui")
        self.close()

    def closeEvent(self, ev):
        pw = self.parentWidget()
        if pw and pw.inherits("QDockWidget"):
            pw.deleteLater()
