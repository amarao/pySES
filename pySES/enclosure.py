#!/usr/bin/python
import os
from .slot import Slot
from .utils import readattr

class EnclosureException(Exception):
    pass

class Enclosure(object):
    _skip_list = ['device', 'power', 'subsystem']
    slots = []
    def _is_enclosure(self, path):
        '''
            check if enclosure is really an enclosure
        '''
        return os.path.isdir(os.path.join(path, 'device', 'enclosure'))


    def _devread(self,path, name):
        fullpath = os.path.join(path , 'device', name)
        return file(fullpath, 'r').read().strip()

    def _fill_enclosure_info(self):
        self.name = os.path.split(self.path)[-1]
        self.vendor = readattr(self.path, 'device/vendor')
        self.model = readattr(self.path, 'device/model')
        self.eh_timeout = readattr(self.path, 'device/eh_timeout')
        self.sas_address = readattr(self.path, 'device/sas_address')
        self.sas_device_handle = readattr(self.path, 'device/sas_device_handle')
        self.sg = os.listdir(os.path.join(self.path, 'device/scsi_generic'))[0]

    def __init__(self, path):
        if not self._is_enclosure(path):
            raise EnclosureException("Not an enclosure")
        self.path = path
        self._fill_enclosure_info()
        for el in os.listdir(path):
            if el in self._skip_list:
                continue
            if not os.path.isdir(os.path.join(self.path, el)):
                continue
            self.slots.append(Slot(self.path, el))

    def __str__(self):
        return "Enclosure %s %s %s (%s slots)" % (
            self.name,
            self.model,
            self.vendor,
            len(self.slots)
        )

