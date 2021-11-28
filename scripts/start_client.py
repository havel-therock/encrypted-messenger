import os
import sys
from pathlib import Path
from messenger.client.test_client import TestClient

if __name__ == "__main__":
    # SETUP
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = Path(dir_path)
    sys.path.append(path.parent.absolute())
    # END OF SETUP

    client = TestClient()
    client.start()
    #  client.send_LOGIN_request()
