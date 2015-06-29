#!/usr/bin/python
import os
from .disk import Disk
#from .slot import Slot
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


    def _slotread(self, path, slot, name):
        fullpath = os.path.join(path, slot, name)
        return file(fullpath, 'r').read().strip()

    def _fill_enclosure_info(self):
        self.name = os.path.split(self.path)[-1]
        self.vendor = self._devread(self.path, 'vendor')
        self.model = self._devread(self.path, 'model')
        self.eh_timeout = self._devread(self.path, 'eh_timeout')
        self.sas_address = self._devread(self.path, 'sas_address')
        self.sas_device_handle = self._devread(self.path, 'sas_device_handle')
        self.sg = os.listdir(os.path.join(self.path, 'device/scsi_generic'))[0]

    def _get_slot_info(self, slot):
        dev = {'slot': slot}
        dev['active'] = self._slotread(self.path, slot, 'active')
        dev['fault'] = self._slotread(self.path, slot, 'fault')
        dev['locate'] = self._slotread(self.path, slot, 'locate')
        dev['disk'] = Disk(os.path.join(self.path, slot, 'device'))
        return dev

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
            self.slots.append(self._get_slot_info(el))

    def __str__(self):
        return "Enclosure %s %s %s (%s slots)" % (
            self.name,
            self.model,
            self.vendor,
            len(self.slots)
        )

