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
    from messenger.client.client import Client
    # END OF IMPORTS

    client = Client()
    client.start()
    #  client.send_LOGIN_request()
