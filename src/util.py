import os
import shutil

def getPath(filename) -> str:
    return os.path.join(os.path.dirname(__file__), filename)

def saveAs(src, dst):
        shutil.copy(src, dst)