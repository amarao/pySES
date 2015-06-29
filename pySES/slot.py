from .utils import readattr
import os
from .disk import Disk
class Slot(object):
    '''
        class Slot describes slots in enclosure.
        Slot may or may not contain one disk, and
        has indicators (fault/location).
    '''
    def _slotread(self, path, slot, name):
        fullpath = os.path.join(path, slot, name)
        return file(fullpath, 'r').read().strip()

    def __init__(self, enclosure_path, slot_name):
        self.name = slot_name
        self.path = os.path.join(enclosure_path, slot_name)
        self.active = readattr(self.path, 'active')
        self.fault_led = readattr(self.path, 'fault')
        self.locate_led = readattr(self.path, 'locate')
        self.disk_present = True  # FIXME!
        self.disk = Disk(os.path.join(enclosure_path, slot_name, 'device'))
 
    def __str__(self):
        return self.name
