# Copyright CEA (2018)

# http://www.cea.fr/

# This software is a computer program whose purpose is to provide an
# Automatic GUI generation for easy dataset editing and display with
# Python.

# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

"""
plotpy.gui.widgets.console
==========================

This module provides a Python console.

.. autoclass:: DockableConsole
"""


from plotpy.console.widgets.internalshell import InternalShell
from plotpy.gui.widgets.dockables import DockableWidgetMixin
from plotpy.gui.widgets.ext_gui_lib import QFont, Qt


class DockableConsole(InternalShell, DockableWidgetMixin):
    """
    Python console that run an interactive shell linked to
    the running process.

    :param parent: parent Qt widget
    :param namespace: available python namespace when the console start
    :type namespace: dict
    :param message: banner displayed before the first prompt
    :param commands: commands run when the interpreter starts
    :param type commands: list of string
    """

    LOCATION = Qt.BottomDockWidgetArea

    def __init__(self, parent, namespace, message, commands=None):
        InternalShell.__init__(
            self,
            parent=parent,
            namespace=namespace,
            message=message,
            commands=commands or [],
            multithreaded=True,
        )
        DockableWidgetMixin.__init__(self, parent)
        self._setup()

    def _setup(self):
        """Setup the calltip widget and show the console once all
        internal handler are ready."""
        font = QFont("Courier new")
        font.setPointSize(10)
        self.set_font(font)
        self.set_codecompletion_auto(True)
        self.set_calltips(True)
        self.setup_completion(size=(300, 180), font=font)
        try:
            self.traceback_available.connect(self._show_console)
        except AttributeError:
            pass

    def _show_console(self):
        """Show the console widget."""
        self.dockwidget.raise_()
        self.dockwidget.show()
