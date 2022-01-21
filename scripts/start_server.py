#!/usr/bin/env python3
import os
import sys
from pathlib import Path


if __name__ == "__main__":
    # SETUP
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = Path(dir_path)
    sys.path.append(str(path.parent.absolute()) + "/")
    # print(sys.path)
    # END OF SETUP
    # IMPORTS
    from messenger.server.server import Server
    # END OF IMPORTS

    # Starting server
    server = Server()
    server.start()



