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

import sys
from PySide2 import QtWidgets

from code_bimtester.guiwidget import TaskPanelBimTester


"""
# this module has to be here and not inside the code_bimtester package
# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3

# outside FreeCAD in a shell
python3 /home/hugo/.FreeCAD/Mod/bimtester/guistartbimtester.py


# outside FreeCAD inside Python
import sys
sys.path.append("/home/hugo/.FreeCAD/Mod/bimtester/")
from  guistartbimtester import show_widget
show_widget()


# inside FreeCAD
import sys
from PySide2 import QtWidgets
from code_bimtester.guiwidget import TaskPanelBimTester
app = QtWidgets.QApplication(sys.argv)
form = TaskPanelBimTester()
form.show()
# sys.exit(app.exec_())

"""


def show_widget():

    # Create the Qt Application
    app = QtWidgets.QApplication(sys.argv)

    # Create and show the form
    form = TaskPanelBimTester()
    form.show()

    # Run the main Qt loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    show_widget()
