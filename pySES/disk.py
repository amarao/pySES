class Disk(dict):
    def __init__(self, path):
        dict.__init__(self)
        self['path'] = path
