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
plotpy.gui.dataset.qtitemwidgets
================================

Widget factories used to edit data items
(factory registration is done in plotpy.gui.dataset.qtwidgets)
(data item types are defined in plotpy.gui.dataset.datatypes)

There is one widget type for each data item type.
Example: ChoiceWidget <--> ChoiceItem, ImageChoiceItem
"""

import collections
import datetime
import os
import os.path as osp
import sys
from gettext import gettext as _

import numpy

from plotpy.core.utils.dataset import restore_dataset, update_dataset
from plotpy.core.utils.strings import utf8_to_unicode
from plotpy.gui.config.misc import get_icon, get_image_file_path, get_image_layout
from plotpy.gui.utils.icons import get_std_icon
from plotpy.gui.utils.misc import text_to_qcolor
from plotpy.gui.widgets.dialog import get_existing_directory
from plotpy.gui.widgets.ext_gui_lib import (
    QCheckBox,
    QColor,
    QColorDialog,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QIcon,
    QLabel,
    QLineEdit,
    QPixmap,
    QPushButton,
    QRadioButton,
    QSlider,
    Qt,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
)
from plotpy.gui.widgets.variableexplorer import arrayeditor

try:
    # PyQt4 4.3.3 on Windows (static DLLs) with py2exe installed:
    # -> pythoncom must be imported first, otherwise py2exe's boot_com_servers
    #    will raise an exception ("Unable to load DLL [...]") when calling any
    #    of the QFileDialog static methods (getOpenFileName, ...)
    import pythoncom
except ImportError:
    pass


# ========================== <!> IMPORTANT <!> =================================
#
# In this module, `item` is an instance of DataItemVariable (not DataItem)
# (see plotpy.core.dataset.datatypes for details)
#
# XXX: consider providing an interface here...


class AbstractDataSetWidget(object):
    """
    Base class for "widgets" handled by `DataSetEditLayout` and it's derived
    classes.

    This is a generic representation of an input (or display) widget that
    has a label and one or more entry field.

    `DataSetEditLayout` uses a registry of *Item* to *Widget* mapping in order
    to automatically create a GUI for a `DataSet` structure
    """

    READ_ONLY = False

    def __init__(self, item, parent_layout):
        """Derived constructors should create the necessary widgets
        The base class keeps a reference to item and parent
        """
        self.item = item
        self.parent_layout = parent_layout
        self.group = None  # Layout/Widget grouping items
        self.label = None
        self.build_mode = False

    def place_label(self, layout, row, column):
        """
        Place item label on layout at specified position (row, column)
        """
        label_text = self.item.get_prop_value("display", "label")
        unit = self.item.get_prop_value("display", "unit", "")
        if unit and not self.READ_ONLY:
            label_text += " ({})".format(unit)
        self.label = QLabel(label_text)
        self.label.setToolTip(self.item.get_help())
        layout.addWidget(self.label, row, column)

    def place_on_grid(
        self, layout, row, label_column, widget_column, row_span=1, column_span=1
    ):
        """
        Place widget on layout at specified position
        """
        self.place_label(layout, row, label_column)
        layout.addWidget(self.group, row, widget_column, row_span, column_span)

    def is_active(self):
        """
        Return True if associated item is active
        """
        return self.item.get_prop_value("display", "active", True)

    def check(self):
        """
        Item validator
        """
        return True

    def set(self):
        """
        Update data item value from widget contents
        """
        # XXX: consider using item.set instead of item.set_from_string...
        self.item.set_from_string(self.value())

    def get(self):
        """
        Update widget contents from data item value
        """
        pass

    def value(self):
        """
        Returns the widget's current value
        """
        return None

    def set_state(self):
        """
        Update the visual status of the widget
        """
        active = self.is_active()
        if self.group:
            self.group.setEnabled(active)
        if self.label:
            self.label.setEnabled(active)


class GroupWidget(AbstractDataSetWidget):
    """
    GroupItem widget
    """

    def __init__(self, item, parent_layout):
        super(GroupWidget, self).__init__(item, parent_layout)
        embedded = item.get_prop_value("display", "embedded", False)
        if not embedded:
            self.group = QGroupBox(item.get_prop_value("display", "label"))
        else:
            self.group = QFrame()
        self.layout = QGridLayout()
        EditLayoutClass = parent_layout.__class__
        self.edit = EditLayoutClass(
            self.group, item.instance, self.layout, item.item.group
        )
        self.group.setLayout(self.layout)

    def get(self):
        """Override AbstractDataSetWidget method"""
        self.edit.update_widgets()

    def set(self):
        """Override AbstractDataSetWidget method"""
        self.edit.accept_changes()

    def check(self):
        """Override AbstractDataSetWidget method"""
        return self.edit.check_all_values()

    def place_on_grid(
        self, layout, row, label_column, widget_column, row_span=1, column_span=1
    ):
        """Override AbstractDataSetWidget method"""
        layout.addWidget(self.group, row, label_column, row_span, column_span + 1)


class TabGroupWidget(AbstractDataSetWidget):
    """

    """

    def __init__(self, item, parent_layout):
        super(TabGroupWidget, self).__init__(item, parent_layout)
        self.tabs = QTabWidget()
        items = item.item.group
        self.widgets = []
        for item in items:
            if item.get_prop_value("display", parent_layout.instance, "hide", False):
                continue
            item.set_prop("display", embedded=True)
            widget = parent_layout.build_widget(item)
            frame = QFrame()
            label = widget.item.get_prop_value("display", "label")
            icon = widget.item.get_prop_value("display", "icon", None)
            if icon is not None:
                self.tabs.addTab(frame, get_icon(icon), label)
            else:
                self.tabs.addTab(frame, label)
            layout = QGridLayout()
            layout.setAlignment(Qt.AlignTop)
            frame.setLayout(layout)
            widget.place_on_grid(layout, 0, 0, 1)
            try:
                widget.get()
            except Exception:
                print("Error building item :", item.item._name)
                raise
            self.widgets.append(widget)

    def get(self):
        """Override AbstractDataSetWidget method"""
        for widget in self.widgets:
            widget.get()

    def set(self):
        """Override AbstractDataSetWidget method"""
        for widget in self.widgets:
            widget.set()

    def check(self):
        """Override AbstractDataSetWidget method"""
        return True

    def place_on_grid(
        self, layout, row, label_column, widget_column, row_span=1, column_span=1
    ):
        """Override AbstractDataSetWidget method"""
        layout.addWidget(self.tabs, row, label_column, row_span, column_span + 1)


class LineEditWidget(AbstractDataSetWidget):
    """
    QLineEdit-based widget
    """

    def __init__(self, item, parent_layout):
        super(LineEditWidget, self).__init__(item, parent_layout)
        self.edit = self.group = QLineEdit()
        self.edit.setToolTip(item.get_help())
        if hasattr(item, "min_equals_max") and item.min_equals_max():
            if item.check_item():
                self.edit.setEnabled(False)
            self.edit.setToolTip(_("Value is forced to {}").format(item.get_max()))
        self.edit.textChanged.connect(self.line_edit_changed)

    def get(self):
        """Override AbstractDataSetWidget method"""
        value = self.item.get()
        old_value = str(self.value())
        if value is not None:
            if isinstance(value, QColor):  # if item is a ColorItem object
                value = value.name()
            uvalue = utf8_to_unicode(value)
            if uvalue != old_value:
                self.edit.setText(utf8_to_unicode(value))
        else:
            self.line_edit_changed(value)

    def line_edit_changed(self, qvalue):
        """QLineEdit validator"""
        if qvalue is not None:
            value = self.item.from_string(str(qvalue))
        else:
            value = None
        if not self.item.check_value(value):
            self.edit.setStyleSheet("background-color:rgb(255, 175, 90);")
        else:
            self.edit.setStyleSheet("")
            cb = self.item.get_prop_value("display", "callback", None)
            if cb is not None:
                if self.build_mode:
                    self.set()
                else:
                    self.parent_layout.update_dataitems()
                cb(self.item.instance, self.item.item, value)
                self.parent_layout.update_widgets(except_this_one=self)
        self.update(value)

    def update(self, value):
        """Override AbstractDataSetWidget method"""
        cb = self.item.get_prop_value("display", "value_callback", None)
        if cb is not None:
            cb(value)

    def value(self):
        """

        :return:
        """
        return str(self.edit.text())

    def check(self):
        """Override AbstractDataSetWidget method"""
        value = self.item.from_string(str(self.edit.text()))
        return self.item.check_value(value)


class TextEditWidget(AbstractDataSetWidget):
    """
    QTextEdit-based widget
    """

    def __init__(self, item, parent_layout):
        super(TextEditWidget, self).__init__(item, parent_layout)
        self.edit = self.group = QTextEdit()
        self.edit.setToolTip(item.get_help())
        if hasattr(item, "min_equals_max") and item.min_equals_max():
            if item.check_item():
                self.edit.setEnabled(False)
            self.edit.setToolTip(_("Value is forced to {}").format(item.get_max()))
        self.edit.textChanged.connect(self.text_changed)

    def __get_text(self):
        """Get QTextEdit text, replacing UTF-8 EOL chars by os.linesep"""
        return str(self.edit.toPlainText()).replace("\u2029", os.linesep)

    def get(self):
        """Override AbstractDataSetWidget method"""
        value = self.item.get()
        if value is not None:
            self.edit.setPlainText(utf8_to_unicode(value))
        self.text_changed()

    def text_changed(self):
        """QLineEdit validator"""
        value = self.item.from_string(self.__get_text())
        if not self.item.check_value(value):
            self.edit.setStyleSheet("background-color:rgb(255, 175, 90);")
        else:
            self.edit.setStyleSheet("")
        self.update(value)

    def update(self, value):
        """Override AbstractDataSetWidget method"""
        pass

    def value(self):
        """
        Returns the widget's current value

        :rtype str:
        """
        return self.edit.toPlainText()

    def check(self):
        """Override AbstractDataSetWidget method"""
        value = self.item.from_string(self.__get_text())
        return self.item.check_value(value)


class CheckBoxWidget(AbstractDataSetWidget):
    """
    BoolItem widget
    """

    def __init__(self, item, parent_layout):
        super(CheckBoxWidget, self).__init__(item, parent_layout)
        self.checkbox = QCheckBox(self.item.get_prop_value("display", "text"))
        self.checkbox.setToolTip(item.get_help())
        self.group = self.checkbox

        self.store = self.item.get_prop("display", "store", None)
        if self.store:
            self.checkbox.stateChanged.connect(self.do_store)

    def get(self):
        """Override AbstractDataSetWidget method"""
        value = self.item.get()
        if value is not None:
            self.checkbox.setChecked(value)

    def set(self):
        """Override AbstractDataSetWidget method"""
        self.item.set(self.value())

    def value(self):
        """
        Returns the widget's current value

        :rtype bool:
        """
        return self.checkbox.isChecked()

    def place_on_grid(
        self, layout, row, label_column, widget_column, row_span=1, column_span=1
    ):
        """Override AbstractDataSetWidget method"""
        if not self.item.get_prop_value("display", "label"):
            widget_column = label_column
            column_span += 1
        else:
            self.place_label(layout, row, label_column)
        layout.addWidget(self.group, row, widget_column, row_span, column_span)

    def do_store(self, state):
        """

        :param state:
        """
        self.store.set(self.item.instance, self.item.item, state)
        self.parent_layout.refresh_widgets()


class DateWidget(AbstractDataSetWidget):
    """
    DateItem widget
    """

    def __init__(self, item, parent_layout):
        super(DateWidget, self).__init__(item, parent_layout)
        self.dateedit = self.group = QDateEdit()
        self.dateedit.setToolTip(item.get_help())

    def get(self):
        """Override AbstractDataSetWidget method"""
        value = self.item.get()
        if value:
            if not isinstance(value, datetime.date):
                value = datetime.date.fromordinal(value)
            self.dateedit.setDate(value)

    def set(self):
        """Override AbstractDataSetWidget method"""
        self.item.set(self.value())

    def value(self):
        """
        Returns the widget's current value

        :rtype date:
        """
        return self.dateedit.date().toPyDate()


class DateTimeWidget(AbstractDataSetWidget):
    """
    DateTimeItem widget
    """

    def __init__(self, item, parent_layout):
        super(DateTimeWidget, self).__init__(item, parent_layout)
        self.dateedit = self.group = QDateTimeEdit()
        self.dateedit.setCalendarPopup(True)
        self.dateedit.setToolTip(item.get_help())

    def get(self):
        """Override AbstractDataSetWidget method"""
        value = self.item.get()
        if value:
            if not isinstance(value, datetime.datetime):
                value = datetime.datetime.fromtimestamp(value)
            self.dateedit.setDateTime(value)

    def set(self):
        """Override AbstractDataSetWidget method"""
        self.item.set(self.value())

    def value(self):
        """
        Returns the widget's current value

        :rtype datetime:
        """
        return self.dateedit.dateTime().toPyDateTime()


class GroupLayout(QHBoxLayout):
    """

    """

    def __init__(self):
        QHBoxLayout.__init__(self)
        self.widgets = []

    def addWidget(self, widget):
        """

        :param widget:
        """
        QHBoxLayout.addWidget(self, widget)
        self.widgets.append(widget)

    def setEnabled(self, state):
        """

        :param state:
        """
        for widget in self.widgets:
            widget.setEnabled(state)


class HLayoutMixin(object):
    """

    """

    def __init__(self, item, parent_layout):
        super(HLayoutMixin, self).__init__(item, parent_layout)
        old_group = self.group
        self.group = GroupLayout()
        self.group.addWidget(old_group)

    def place_on_grid(
        self, layout, row, label_column, widget_column, row_span=1, column_span=1
    ):
        """Override AbstractDataSetWidget method"""
        self.place_label(layout, row, label_column)
        layout.addLayout(self.group, row, widget_column, row_span, column_span)


class ColorWidget(HLayoutMixin, LineEditWidget):
    """
    ColorItem widget
    """

    def __init__(self, item, parent_layout):
        super(ColorWidget, self).__init__(item, parent_layout)
        self.button = QPushButton("")
        self.button.setMaximumWidth(32)
        self.button.clicked.connect(self.select_color)
        self.group.addWidget(self.button)

    def update(self, value):
        """Reimplement LineEditWidget method"""
        LineEditWidget.update(self, value)
        color = text_to_qcolor(value)
        if color.isValid():
            bitmap = QPixmap(16, 16)
            bitmap.fill(color)
            icon = QIcon(bitmap)
        else:
            icon = get_icon("not_found")
        self.button.setIcon(icon)

    def select_color(self):
        """Open a color selection dialog box"""
        color = text_to_qcolor(self.edit.text())
        if not color.isValid():
            color = Qt.gray
        color = QColorDialog.getColor(color, self.parent_layout.parent)
        if color.isValid():
            value = color.name()
            self.edit.setText(value)
            self.update(value)


class SliderWidget(HLayoutMixin, LineEditWidget):
    """
    IntItem with Slider
    """

    DATA_TYPE = int

    def __init__(self, item, parent_layout):
        super(SliderWidget, self).__init__(item, parent_layout)
        self.slider = self.vmin = self.vmax = None
        if item.get_prop_value("display", "slider"):
            self.vmin = item.get_prop_value("data", "min")
            self.vmax = item.get_prop_value("data", "max")
            assert (
                self.vmin is not None and self.vmax is not None
            ), "SliderWidget requires that item min/max have been defined"
            self.slider = QSlider()
            self.slider.setOrientation(Qt.Horizontal)
            self.setup_slider(item)
            self.slider.valueChanged.connect(self.value_changed)
            self.group.addWidget(self.slider)

    def value_to_slider(self, value):
        """

        :param value:
        :return:
        """
        return max(min(value, self.vmax), self.vmin)

    def slider_to_value(self, value):
        """

        :param value:
        :return:
        """
        return value

    def setup_slider(self, item):
        """

        :param item:
        """
        self.slider.setRange(self.vmin, self.vmax)

    def update(self, value):
        """Reimplement LineEditWidget method"""
        LineEditWidget.update(self, value)
        if self.slider is not None and isinstance(value, self.DATA_TYPE):
            self.slider.blockSignals(True)
            self.slider.setValue(self.value_to_slider(value))
            self.slider.blockSignals(False)

    def value_changed(self, ivalue):
        """Update the lineedit"""
        value = str(self.slider_to_value(ivalue))
        self.edit.setText(value)
        self.update(value)


class FloatSliderWidget(SliderWidget):
    """
    FloatItem with Slider
    """

    DATA_TYPE = float

    def value_to_slider(self, value):
        """

        :param value:
        :return:
        """
        value_percent = (value - self.vmin) * 100 / (self.vmax - self.vmin)
        return max(min(value_percent, 100), 0)

    def slider_to_value(self, value):
        """

        :param value:
        :return:
        """
        return value * (self.vmax - self.vmin) / 100 + self.vmin

    def setup_slider(self, item):
        """

        :param item:
        """
        self.slider.setRange(0, 100)


def _get_child_title_func(ancestor):
    previous_ancestor = None
    while True:
        try:
            if previous_ancestor is ancestor:
                break
            return ancestor.child_title
        except AttributeError:
            previous_ancestor = ancestor
            ancestor = ancestor.parent()
    return lambda item: ""


class FileWidget(HLayoutMixin, LineEditWidget):
    """
    File path item widget
    """

    def __init__(self, item, parent_layout, filedialog):
        super(FileWidget, self).__init__(item, parent_layout)
        self.filedialog = filedialog
        button = QPushButton()
        fmt = item.get_prop_value("data", "formats")
        button.setIcon(get_icon("{}.png".format(fmt[0].lower()), default="file.png"))
        button.clicked.connect(self.select_file)
        self.group.addWidget(button)
        self.basedir = item.get_prop_value("data", "basedir")
        self.all_files_first = item.get_prop_value("data", "all_files_first")

    def select_file(self):
        """Open a file selection dialog box"""
        fname = self.item.from_string(str(self.edit.text()))
        if isinstance(fname, list):
            fname = osp.dirname(fname[0])
        parent = self.parent_layout.parent
        _temp = sys.stdout
        sys.stdout = None
        if len(fname) == 0:
            fname = self.basedir
        _formats = self.item.get_prop_value("data", "formats")
        formats = [str(format).lower() for format in _formats]
        filter_lines = [
            (_("{} files") + " (*.{})").format(format.upper(), format)
            for format in formats
        ]
        all_filter = _("All supported files") + " (*.{})".format(" *.".join(formats))
        if len(formats) > 1:
            if self.all_files_first:
                filter_lines.insert(0, all_filter)
            else:
                filter_lines.append(all_filter)
        if fname is None:
            fname = ""
        child_title = _get_child_title_func(parent)
        fname, _filter = self.filedialog(
            parent, child_title(self.item), fname, "\n".join(filter_lines)
        )
        sys.stdout = _temp
        if fname:
            if isinstance(fname, list):
                fname = str(fname)
            self.edit.setText(fname)


class DirectoryWidget(HLayoutMixin, LineEditWidget):
    """
    Directory path item widget
    """

    def __init__(self, item, parent_layout):
        super(DirectoryWidget, self).__init__(item, parent_layout)
        button = QPushButton()
        button.setIcon(get_std_icon("DirOpenIcon"))
        button.clicked.connect(self.select_directory)
        self.group.addWidget(button)

    def select_directory(self):
        """Open a directory selection dialog box"""
        value = self.item.from_string(str(self.edit.text()))
        parent = self.parent_layout.parent
        child_title = _get_child_title_func(parent)
        dname = get_existing_directory(parent, child_title(self.item), value)
        if dname:
            self.edit.setText(dname)


class ChoiceWidget(AbstractDataSetWidget):
    """
    Choice item widget
    """

    def __init__(self, item, parent_layout):
        super(ChoiceWidget, self).__init__(item, parent_layout)
        self._first_call = True
        self.is_radio = item.get_prop_value("display", "radio")
        self.store = self.item.get_prop("display", "store", None)
        if self.is_radio:
            self.group = QGroupBox()
            self.group.setToolTip(item.get_help())
            self.vbox = QVBoxLayout()
            self.group.setLayout(self.vbox)
            self._buttons = []
        else:
            self.combobox = self.group = QComboBox()
            self.combobox.setToolTip(item.get_help())
            self.combobox.currentIndexChanged.connect(self.index_changed)

    def index_changed(self, index):
        """

        :param index:
        """
        if self.store:
            self.store.set(self.item.instance, self.item.item, self.value())
            self.parent_layout.refresh_widgets()
        cb = self.item.get_prop_value("display", "callback", None)
        if cb is not None:
            if self.build_mode:
                self.set()
            else:
                self.parent_layout.update_dataitems()
            cb(self.item.instance, self.item.item, self.value())
            self.parent_layout.update_widgets(except_this_one=self)

    def initialize_widget(self):
        """

        """
        if self.is_radio:
            for button in self._buttons:
                button.toggled.disconnect(self.index_changed)
                self.vbox.removeWidget(button)
                button.deleteLater()
            self._buttons = []
        else:
            self.combobox.blockSignals(True)
            while self.combobox.count():
                self.combobox.removeItem(0)
        _choices = self.item.get_prop_value("data", "choices")
        for key, lbl, img in _choices:
            if self.is_radio:
                button = QRadioButton(lbl, self.group)
            if img:
                if isinstance(img, str):
                    if not osp.isfile(img):
                        img = get_image_file_path(img)
                    img = QIcon(img)
                elif isinstance(img, collections.Callable):
                    img = img(key)
                if self.is_radio:
                    button.setIcon(img)
                else:
                    self.combobox.addItem(img, lbl)
            elif not self.is_radio:
                self.combobox.addItem(lbl)
            if self.is_radio:
                self._buttons.append(button)
                self.vbox.addWidget(button)
                button.toggled.connect(self.index_changed)
        if not self.is_radio:
            self.combobox.blockSignals(False)

    def set_widget_value(self, idx):
        """

        :param idx:
        """
        if self.is_radio:
            for button in self._buttons:
                button.blockSignals(True)
            self._buttons[idx].setChecked(True)
            for button in self._buttons:
                button.blockSignals(False)
        else:
            self.combobox.blockSignals(True)
            self.combobox.setCurrentIndex(idx)
            self.combobox.blockSignals(False)

    def get_widget_value(self):
        """

        :return:
        """
        if self.is_radio:
            for index, widget in enumerate(self._buttons):
                if widget.isChecked():
                    return index
        else:
            return self.combobox.currentIndex()

    def get(self):
        """Override AbstractDataSetWidget method"""
        self.initialize_widget()
        value = self.item.get()
        if value is not None:
            idx = 0
            _choices = self.item.get_prop_value("data", "choices")
            for key, _val, _img in _choices:
                if key == value:
                    break
                idx += 1
            self.set_widget_value(idx)
            if self._first_call:
                self.index_changed(idx)
                self._first_call = False

    def set(self):
        """Override AbstractDataSetWidget method"""
        try:
            value = self.value()
        except IndexError:
            return
        self.item.set(value)

    def value(self):
        """

        :return:
        """
        index = self.get_widget_value()
        choices = self.item.get_prop_value("data", "choices")
        return choices[index][0]


class MultipleChoiceWidget(AbstractDataSetWidget):
    """
    Multiple choice item widget
    """

    def __init__(self, item, parent_layout):
        super(MultipleChoiceWidget, self).__init__(item, parent_layout)
        self.groupbox = self.group = QGroupBox(item.get_prop_value("display", "label"))
        layout = QGridLayout()
        self.boxes = []
        nx, ny = item.get_prop_value("display", "shape")
        cx, cy = 0, 0
        _choices = item.get_prop_value("data", "choices")
        for _, choice, _img in _choices:
            checkbox = QCheckBox(choice)
            layout.addWidget(checkbox, cx, cy)
            if nx < 0:
                cy += 1
                if cy >= ny:
                    cy = 0
                    cx += 1
            else:
                cx += 1
                if cx >= nx:
                    cx = 0
                    cy += 1
            self.boxes.append(checkbox)
        self.groupbox.setLayout(layout)

    def get(self):
        """Override AbstractDataSetWidget method"""
        value = self.item.get()
        _choices = self.item.get_prop_value("data", "choices")
        for (i, _choice, _img), checkbox in zip(_choices, self.boxes):
            if value is not None and i in value:
                checkbox.setChecked(True)

    def set(self):
        """Override AbstractDataSetWidget method"""
        _choices = self.item.get_prop_value("data", "choices")
        choices = [_choices[i][0] for i in self.value()]
        self.item.set(choices)

    def value(self):
        """

        :return:
        """
        return [i for i, w in enumerate(self.boxes) if w.isChecked()]

    def place_on_grid(
        self, layout, row, label_column, widget_column, row_span=1, column_span=1
    ):
        """Override AbstractDataSetWidget method"""
        layout.addWidget(self.group, row, label_column, row_span, column_span + 1)


class FloatArrayWidget(AbstractDataSetWidget):
    """
    FloatArrayItem widget
    """

    def __init__(self, item, parent_layout):
        super(FloatArrayWidget, self).__init__(item, parent_layout)
        _label = item.get_prop_value("display", "label")
        self.groupbox = self.group = QGroupBox(_label)
        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignLeft)
        self.groupbox.setLayout(self.layout)

        self.first_line, self.dim_label = get_image_layout(
            "shape.png", _("Number of rows x Number of columns")
        )
        edit_button = QPushButton(get_icon("arredit.png"), "")
        edit_button.setToolTip(_("Edit array contents"))
        edit_button.setMaximumWidth(32)
        self.first_line.addWidget(edit_button)
        self.layout.addLayout(self.first_line, 0, 0)

        self.min_line, self.min_label = get_image_layout(
            "min.png", _("Smallest element in array")
        )
        self.layout.addLayout(self.min_line, 1, 0)
        self.max_line, self.max_label = get_image_layout(
            "max.png", _("Largest element in array")
        )
        self.layout.addLayout(self.max_line, 2, 0)

        edit_button.clicked.connect(self.edit_array)
        self.arr = None  # le tableau si il a été modifié
        self.instance = None

    def edit_array(self):
        """Open an array editor dialog"""
        parent = self.parent_layout.parent
        label = self.item.get_prop_value("display", "label")
        editor = arrayeditor.ArrayEditor(parent)
        if editor.setup_and_check(self.arr, title=label):
            if editor.exec_():
                self.update(self.arr)

    def get(self):
        """Override AbstractDataSetWidget method"""
        self.arr = numpy.array(self.item.get(), copy=False)
        if self.item.get_prop_value("display", "transpose"):
            self.arr = self.arr.T
        self.update(self.arr)

    def update(self, arr):
        """Override AbstractDataSetWidget method"""
        shape = arr.shape
        if len(shape) == 1:
            shape = (1,) + shape
        dim = " x ".join([str(d) for d in shape])
        self.dim_label.setText(dim)

        format = self.item.get_prop_value("display", "format")
        minmax = self.item.get_prop_value("display", "minmax")
        try:
            if minmax == "all":
                mint = format % arr.min()
                maxt = format % arr.max()
            elif minmax == "columns":
                mint = ", ".join(
                    [format % arr[r, :].min() for r in range(arr.shape[0])]
                )
                maxt = ", ".join(
                    [format % arr[r, :].max() for r in range(arr.shape[0])]
                )
            else:
                mint = ", ".join(
                    [format % arr[:, r].min() for r in range(arr.shape[1])]
                )
                maxt = ", ".join(
                    [format % arr[:, r].max() for r in range(arr.shape[1])]
                )
        except (TypeError, IndexError):
            mint, maxt = "-", "-"
        self.min_label.setText(mint)
        self.max_label.setText(maxt)

    def set(self):
        """Override AbstractDataSetWidget method"""
        if self.item.get_prop_value("display", "transpose"):
            value = self.value().T
        else:
            value = self.value()
        self.item.set(value)

    def value(self):
        """

        :return:
        """
        return self.arr

    def place_on_grid(
        self, layout, row, label_column, widget_column, row_span=1, column_span=1
    ):
        """Override AbstractDataSetWidget method"""
        layout.addWidget(self.group, row, label_column, row_span, column_span + 1)


class ButtonWidget(AbstractDataSetWidget):
    """
    BoolItem widget
    """

    def __init__(self, item, parent_layout):
        super(ButtonWidget, self).__init__(item, parent_layout)
        _label = self.item.get_prop_value("display", "label")
        self.button = self.group = QPushButton(_label)
        self.button.setToolTip(item.get_help())
        _icon = self.item.get_prop_value("display", "icon")
        if _icon is not None:
            if isinstance(_icon, str):
                _icon = get_icon(_icon)
            self.button.setIcon(_icon)
        self.button.clicked.connect(self.clicked)
        self.cb_value = None

    def get(self):
        """Override AbstractDataSetWidget method"""
        self.cb_value = self.item.get()

    def set(self):
        """Override AbstractDataSetWidget method"""
        self.item.set(self.value())

    def value(self):
        """

        :return:
        """
        return self.cb_value

    def place_on_grid(
        self, layout, row, label_column, widget_column, row_span=1, column_span=1
    ):
        """Override AbstractDataSetWidget method"""
        layout.addWidget(self.group, row, label_column, row_span, column_span + 1)

    def clicked(self, *args):
        """

        :param args:
        """
        self.parent_layout.update_dataitems()
        callback = self.item.get_prop_value("display", "callback")
        self.cb_value = callback(
            self.item.instance, self.item.item, self.cb_value, self.button.parent()
        )
        self.set()
        self.parent_layout.update_widgets()


class DataSetWidget(AbstractDataSetWidget):
    """
    DataSet widget
    """

    def __init__(self, item, parent_layout):
        super(DataSetWidget, self).__init__(item, parent_layout)
        self.dataset = self.klass()
        # Création du layout contenant les champs d'édition du signal
        embedded = item.get_prop_value("display", "embedded", False)
        if not embedded:
            self.group = QGroupBox(item.get_prop_value("display", "label"))
        else:
            self.group = QFrame()
        self.layout = QGridLayout()
        self.group.setLayout(self.layout)
        EditLayoutClass = parent_layout.__class__
        self.edit = EditLayoutClass(
            self.parent_layout.parent, self.dataset, self.layout
        )

    def get(self):
        """Override AbstractDataSetWidget method"""
        self.get_dataset()
        for widget in self.edit.widgets:
            widget.get()

    def set(self):
        """Override AbstractDataSetWidget method"""
        for widget in self.edit.widgets:
            widget.set()
        self.set_dataset()

    def get_dataset(self):
        """update's internal parameter representation
        from the item's stored value

        default behavior uses update_dataset and assumes
        internal dataset class is the same as item's value
        class"""
        item = self.item.get()
        update_dataset(self.dataset, item)

    def set_dataset(self):
        """update the item's value from the internal
        data representation

        default behavior uses restore_dataset and assumes
        internal dataset class is the same as item's value
        class"""
        item = self.item.get()
        restore_dataset(self.dataset, item)

    def place_on_grid(
        self, layout, row, label_column, widget_column, row_span=1, column_span=1
    ):
        """Override AbstractDataSetWidget method"""
        layout.addWidget(self.group, row, label_column, row_span, column_span + 1)
