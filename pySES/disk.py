import os
class Disk(object):
    model = None
    sas_address = None
    sas_device_handle = None
    timeout = None
    eh_timeout = None
    sg = None


    def _readattr(self, path, attr):
        try:
            return file(os.path.join(path, attr), 'r').read().strip()
        except None:
            return None


    def _getsubdir(self, path, subpath):
        try:
            return os.listdir(os.path.join(path, subpath))[0]
        except:
            return None


    def __init__(self, path):
        self.path = path
        self.name = os.listdir(os.path.join(path, 'block'))[0]
#todo sector_size from queue       self['size'] = self._readattr(os.path.join('block', self['name'], "size"))
        self.model = self._readattr(self.path, 'model')
        self.sas_address = self._readattr(self.path, 'sas_address')
        self.sas_device_handle = self._readattr(self.path, 'sas_device_handle')
        self.timeout = self._readattr(self.path, 'timeout')
        self.eh_timeout = self._readattr(self.path, 'eh_timeout')
        self.sg = os.listdir(os.path.join(path, 'scsi_generic'))[0]

    def __str__(self):
        return ' '.join([self.name, self.model])
