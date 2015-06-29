#!/usr/bin/python
import os
from .disk import Disk
class EnclosureException(Exception):
    pass

class Enclosure(dict):
    _skip_list = ['device', 'power', 'subsystem']
    slot_list = []
    def _is_enclosure(self):
        '''
            check if enclosure is really an enclosure
        '''
        return os.path.isdir(os.path.join(self['path'], 'device', 'enclosure'))


    def _devread(self,name):
        fullpath = os.path.join(self['path'], 'device', name)
        return file(fullpath, 'r').read().strip()


    def _slotread(self,slot,name):
        fullpath = os.path.join(self['path'], slot, name)
        return file(fullpath, 'r').read().strip()

    def _fill_enclosure_info(self):
        self['name'] = os.path.split(self['path'])[-1]
        self['vendor'] = self._devread('vendor')
        self['model'] = self._devread('model')
        self['eh_timeout'] = self._devread('eh_timeout')
        self['sas_address'] = self._devread('sas_address')
        self['rev'] = self._devread('rev')
        self['sas_device_handle'] = self._devread('sas_device_handle')
        self['sg'] = os.listdir(os.path.join(self['path'],'device/scsi_generic'))[0]

    def get_slot_info(self, slot):
        dev = {'slot': slot}
        dev['active'] = self._slotread(slot, 'active')
        dev['fault'] = self._slotread(slot, 'fault')
        dev['locate'] = self._slotread(slot, 'locate')
        dev['disk'] = Disk(os.path.join(self['path'], slot, 'device'))
        return dev

    def __init__(self, path):
        dict.__init__(self)
        self['path'] = path
        if not self._is_enclosure():
            raise EnclosureException("Not an enclosure")
        self._fill_enclosure_info()
        slots = []
        for el in os.listdir(path):
            if el in self._skip_list:
                continue
            if not os.path.isdir(os.path.join(self['path'], el)):
                continue
            slots.append(self.get_slot_info(el))
        self['slots'] = slots

    def __str__(self):
        return "Enclosure %s %s %s (%s slots)" % (
            self["name"],
            self["model"],
            self["vendor"],
            len(self["slots"])
        )

