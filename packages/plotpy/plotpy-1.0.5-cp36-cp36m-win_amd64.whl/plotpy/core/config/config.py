"""


:synopsis:

:moduleauthor: CEA

:platform: All

"""

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
Module plotpy.core.config.config
================================

Handle *plotpy.core* module configuration
(options, images and icons)
"""


import os.path as osp

from plotpy.core.config.misc import add_image_module_path, get_translation
from plotpy.core.config.userconfig import UserConfig

APP_PATH = osp.dirname(__file__)
add_image_module_path("plotpy", "images")
_ = get_translation("plotpy")

DEFAULTS = {
    "arrayeditor": {
        "font/family/nt": ["Consolas", "Courier New"],
        "font/family/posix": "Bitstream Vera Sans Mono",
        "font/family/mac": "Monaco",
        "font/size": 9,
        "font/bold": False,
    },
    "dicteditor": {
        "font/family/nt": ["Consolas", "Courier New"],
        "font/family/posix": "Bitstream Vera Sans Mono",
        "font/family/mac": "Monaco",
        "font/size": 9,
        "font/italic": False,
        "font/bold": False,
    },
    "texteditor": {
        "font/family/nt": ["Consolas", "Courier New"],
        "font/family/posix": "Bitstream Vera Sans Mono",
        "font/family/mac": "Monaco",
        "font/size": 9,
        "font/italic": False,
        "font/bold": False,
    },
    "internal_console": {
        "max_line_count": 300,
        "working_dir_history": 30,
        "working_dir_adjusttocontents": False,
        "wrap": True,
        "calltips": True,
        "codecompletion/size": [300, 100],
        "codecompletion/auto": False,
        "codecompletion/enter_key": True,
        "codecompletion/case_sensitive": True,
        "external_editor/path": "SciTE",
        "external_editor/gotoline": "-goto:",
        "light_background": True,
    },
    "color_schemes": {
        "names": [
            "emacs",
            "idle",
            "monokai",
            "pydev",
            "scintilla",
            "spyder",
            "spyder/dark",
            "zenburn",
            "solarized/light",
            "solarized/dark",
        ],
        "selected": "spyder",
        # ---- Emacs ----
        "emacs/name": "Emacs",
        #      Name            Color     Bold  Italic
        "emacs/background": "#000000",
        "emacs/currentline": "#2b2b43",
        "emacs/currentcell": "#1c1c2d",
        "emacs/occurrence": "#abab67",
        "emacs/ctrlclick": "#0000ff",
        "emacs/sideareas": "#555555",
        "emacs/matched_p": "#009800",
        "emacs/unmatched_p": "#c80000",
        "emacs/normal": ("#ffffff", False, False),
        "emacs/keyword": ("#3c51e8", False, False),
        "emacs/builtin": ("#900090", False, False),
        "emacs/definition": ("#ff8040", True, False),
        "emacs/comment": ("#005100", False, False),
        "emacs/string": ("#00aa00", False, True),
        "emacs/number": ("#800000", False, False),
        "emacs/instance": ("#ffffff", False, True),
        # ---- IDLE ----
        "idle/name": "IDLE",
        #      Name            Color     Bold  Italic
        "idle/background": "#ffffff",
        "idle/currentline": "#f2e6f3",
        "idle/currentcell": "#feefff",
        "idle/occurrence": "#e8f2fe",
        "idle/ctrlclick": "#0000ff",
        "idle/sideareas": "#efefef",
        "idle/matched_p": "#99ff99",
        "idle/unmatched_p": "#ff9999",
        "idle/normal": ("#000000", False, False),
        "idle/keyword": ("#ff7700", True, False),
        "idle/builtin": ("#900090", False, False),
        "idle/definition": ("#0000ff", False, False),
        "idle/comment": ("#dd0000", False, True),
        "idle/string": ("#00aa00", False, False),
        "idle/number": ("#924900", False, False),
        "idle/instance": ("#777777", True, True),
        # ---- Monokai ----
        "monokai/name": "Monokai",
        #      Name              Color     Bold  Italic
        "monokai/background": "#2a2b24",
        "monokai/currentline": "#484848",
        "monokai/currentcell": "#3d3d3d",
        "monokai/occurrence": "#666666",
        "monokai/ctrlclick": "#0000ff",
        "monokai/sideareas": "#2a2b24",
        "monokai/matched_p": "#688060",
        "monokai/unmatched_p": "#bd6e76",
        "monokai/normal": ("#ddddda", False, False),
        "monokai/keyword": ("#f92672", False, False),
        "monokai/builtin": ("#ae81ff", False, False),
        "monokai/definition": ("#a6e22e", False, False),
        "monokai/comment": ("#75715e", False, True),
        "monokai/string": ("#e6db74", False, False),
        "monokai/number": ("#ae81ff", False, False),
        "monokai/instance": ("#ddddda", False, True),
        # ---- Pydev ----
        "pydev/name": "Pydev",
        #      Name            Color     Bold  Italic
        "pydev/background": "#ffffff",
        "pydev/currentline": "#e8f2fe",
        "pydev/currentcell": "#eff8fe",
        "pydev/occurrence": "#ffff99",
        "pydev/ctrlclick": "#0000ff",
        "pydev/sideareas": "#efefef",
        "pydev/matched_p": "#99ff99",
        "pydev/unmatched_p": "#ff99992",
        "pydev/normal": ("#000000", False, False),
        "pydev/keyword": ("#0000ff", False, False),
        "pydev/builtin": ("#900090", False, False),
        "pydev/definition": ("#000000", True, False),
        "pydev/comment": ("#c0c0c0", False, False),
        "pydev/string": ("#00aa00", False, True),
        "pydev/number": ("#800000", False, False),
        "pydev/instance": ("#000000", False, True),
        # ---- Scintilla ----
        "scintilla/name": "Scintilla",
        #         Name             Color     Bold  Italic
        "scintilla/background": "#ffffff",
        "scintilla/currentline": "#e1f0d1",
        "scintilla/currentcell": "#edfcdc",
        "scintilla/occurrence": "#ffff99",
        "scintilla/ctrlclick": "#0000ff",
        "scintilla/sideareas": "#efefef",
        "scintilla/matched_p": "#99ff99",
        "scintilla/unmatched_p": "#ff9999",
        "scintilla/normal": ("#000000", False, False),
        "scintilla/keyword": ("#00007f", True, False),
        "scintilla/builtin": ("#000000", False, False),
        "scintilla/definition": ("#007f7f", True, False),
        "scintilla/comment": ("#007f00", False, False),
        "scintilla/string": ("#7f007f", False, False),
        "scintilla/number": ("#007f7f", False, False),
        "scintilla/instance": ("#000000", False, True),
        # ---- Spyder ----
        "spyder/name": "Spyder",
        #       Name            Color     Bold  Italic
        "spyder/background": "#ffffff",
        "spyder/currentline": "#f7ecf8",
        "spyder/currentcell": "#fdfdde",
        "spyder/occurrence": "#ffff99",
        "spyder/ctrlclick": "#0000ff",
        "spyder/sideareas": "#efefef",
        "spyder/matched_p": "#99ff99",
        "spyder/unmatched_p": "#ff9999",
        "spyder/normal": ("#000000", False, False),
        "spyder/keyword": ("#0000ff", False, False),
        "spyder/builtin": ("#900090", False, False),
        "spyder/definition": ("#000000", True, False),
        "spyder/comment": ("#adadad", False, True),
        "spyder/string": ("#00aa00", False, False),
        "spyder/number": ("#800000", False, False),
        "spyder/instance": ("#924900", False, True),
        # ---- Spyder/Dark ----
        "spyder/dark/name": "Spyder Dark",
        #           Name             Color     Bold  Italic
        "spyder/dark/background": "#131926",
        "spyder/dark/currentline": "#2b2b43",
        "spyder/dark/currentcell": "#31314e",
        "spyder/dark/occurrence": "#abab67",
        "spyder/dark/ctrlclick": "#0000ff",
        "spyder/dark/sideareas": "#282828",
        "spyder/dark/matched_p": "#009800",
        "spyder/dark/unmatched_p": "#c80000",
        "spyder/dark/normal": ("#ffffff", False, False),
        "spyder/dark/keyword": ("#558eff", False, False),
        "spyder/dark/builtin": ("#aa00aa", False, False),
        "spyder/dark/definition": ("#ffffff", True, False),
        "spyder/dark/comment": ("#7f7f7f", False, False),
        "spyder/dark/string": ("#11a642", False, True),
        "spyder/dark/number": ("#c80000", False, False),
        "spyder/dark/instance": ("#be5f00", False, True),
        # ---- Zenburn ----
        "zenburn/name": "Zenburn",
        #        Name            Color     Bold  Italic
        "zenburn/background": "#3f3f3f",
        "zenburn/currentline": "#333333",
        "zenburn/currentcell": "#2c2c2c",
        "zenburn/occurrence": "#7a738f",
        "zenburn/ctrlclick": "#0000ff",
        "zenburn/sideareas": "#3f3f3f",
        "zenburn/matched_p": "#688060",
        "zenburn/unmatched_p": "#bd6e76",
        "zenburn/normal": ("#dcdccc", False, False),
        "zenburn/keyword": ("#dfaf8f", True, False),
        "zenburn/builtin": ("#efef8f", False, False),
        "zenburn/definition": ("#efef8f", False, False),
        "zenburn/comment": ("#7f9f7f", False, True),
        "zenburn/string": ("#cc9393", False, False),
        "zenburn/number": ("#8cd0d3", False, False),
        "zenburn/instance": ("#dcdccc", False, True),
        # ---- Solarized Light ----
        "solarized/light/name": "Solarized Light",
        #        Name            Color     Bold  Italic
        "solarized/light/background": "#fdf6e3",
        "solarized/light/currentline": "#f5efdB",
        "solarized/light/currentcell": "#eee8d5",
        "solarized/light/occurrence": "#839496",
        "solarized/light/ctrlclick": "#d33682",
        "solarized/light/sideareas": "#eee8d5",
        "solarized/light/matched_p": "#586e75",
        "solarized/light/unmatched_p": "#dc322f",
        "solarized/light/normal": ("#657b83", False, False),
        "solarized/light/keyword": ("#859900", False, False),
        "solarized/light/builtin": ("#6c71c4", False, False),
        "solarized/light/definition": ("#268bd2", True, False),
        "solarized/light/comment": ("#93a1a1", False, True),
        "solarized/light/string": ("#2aa198", False, False),
        "solarized/light/number": ("#cb4b16", False, False),
        "solarized/light/instance": ("#b58900", False, True),
        # ---- Solarized Dark ----
        "solarized/dark/name": "Solarized Dark",
        #        Name            Color     Bold  Italic
        "solarized/dark/background": "#002b36",
        "solarized/dark/currentline": "#083f4d",
        "solarized/dark/currentcell": "#073642",
        "solarized/dark/occurrence": "#657b83",
        "solarized/dark/ctrlclick": "#d33682",
        "solarized/dark/sideareas": "#073642",
        "solarized/dark/matched_p": "#93a1a1",
        "solarized/dark/unmatched_p": "#dc322f",
        "solarized/dark/normal": ("#839496", False, False),
        "solarized/dark/keyword": ("#859900", False, False),
        "solarized/dark/builtin": ("#6c71c4", False, False),
        "solarized/dark/definition": ("#268bd2", True, False),
        "solarized/dark/comment": ("#586e75", False, True),
        "solarized/dark/string": ("#2aa198", False, False),
        "solarized/dark/number": ("#cb4b16", False, False),
        "solarized/dark/instance": ("#b58900", False, True),
    },
    "main": {
        "rich_font/italic": False,
        "rich_font/bold": False,
        "cursor/width": 2,
        "completion/size": (300, 180),
        "report_error/remember_me": False,
        "report_error/remember_token": False,
    },
    "shortcuts": {
        # ---- Global ----
        # ---- Editor ----
        # -- In widgets/sourcecode/codeeditor.py,
        "editor/go to new line": "Ctrl+Shift+Return",
        "editor/go to definition": "Ctrl+G",
        "editor/start of line": "Meta+A",
        "editor/end of line": "Meta+E",
        "editor/previous line": "Meta+P",
        "editor/next line": "Meta+N",
        "editor/previous char": "Meta+B",
        "editor/next char": "Meta+F",
        "editor/previous word": "Meta+Left",
        "editor/next word": "Meta+Right",
        "editor/start of document": "Ctrl+Home",
        "editor/end of document": "Ctrl+End",
        "editor/copy": "Ctrl+C",
        "editor/select all": "Ctrl+A",
        # -- In widgets/editor.py
        "editor/go to line": "Ctrl+L",
        "editor/last edit location": "Ctrl+Alt+Shift+Left",
        "editor/previous cursor position": "Ctrl+Alt+Left",
        "editor/next cursor position": "Ctrl+Alt+Right",
        # ---- In widgets/arraybuider.py ----
        "array_builder/enter array inline": "Ctrl+Alt+M",
        "array_builder/enter array table": "Ctrl+M",
        # ---- In widgets/variableexplorer/aarayeditor.py ----
        "variable_explorer/copy": "Ctrl+C",
        # ---- Consoles (in widgets/shell) ----
        "console/inspect current object": "Ctrl+I",
        "console/clear shell": "Ctrl+L",
        "console/clear line": "Shift+Escape",
        # ---- In widgets/arraybuider.py ----
        "array_builder/enter array inline": "Ctrl+Alt+M",
        "array_builder/enter array table": "Ctrl+M",
    },
    "historylog": {"enable": True, "max_entries": 100, "wrap": True, "go_to_eof": True},
}

CONF = UserConfig(DEFAULTS)
