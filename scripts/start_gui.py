#!/usr/bin/env python3
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    # SETUP
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = Path(dir_path)
    sys.path.append(str(path.parent.absolute()) + "/")
    # END OF SETUP
    # IMPORTS
    import messenger.client.gui as gui
    # END OF IMPORTS

    # Starting GUI
    app = gui.QApplication(sys.argv)
    window = gui.Window()
    window.show()
    window.startGUI()
    sys.exit(app.exec_())
