#####
# add top layer of project to search patch for python modules
import os, sys
from pathlib import Path
dir_path = os.path.dirname(os.path.realpath(__file__))
path = Path(dir_path)
sys.path.append(path.parent.absolute())
#####

# dummy import and starting server
# serverside need to align to below convention
'''
import messenger.server.server as server

s = server.Server()
s.start()
'''


