import os
import sys
from pathlib import Path


if __name__ == "__main__":
    # SETUP
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = Path(dir_path)
    sys.path.append(path.parent.absolute())
    # END OF SETUP
