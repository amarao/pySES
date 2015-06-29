import os
def readattr(*paths):
    fullpath = os.path.join(*paths)
    return file(fullpath, 'r').read().strip()
