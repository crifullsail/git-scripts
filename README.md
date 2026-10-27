# Git in VS Code

Let's make some code changes.


Here is the code for Maya to see the new scripts 

import importlib
import sys

script_folder = r"D:\OneDrive - Full Sail University\CGA-3312\rigging_tools\git-scripts"

if script_folder not in sys.path:
    sys.path.insert(0, script_folder)