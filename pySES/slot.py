from .utils import readattr
import os
from .disk import Disk

ENABLE_STRING = '1'

class Slot(object):
    '''
        class Slot describes slots in enclosure.
        Slot may or may not contain one disk, and
        has indicators (fault/location).
    '''
    def _write_attr(self, attr, value):
        f = file(os.path.join(self.path,attr),'w')
        f.write(value)
        del f

    def update(self):
        self.active = readattr(self.path, 'active')
        self.fault_led = bool(int(readattr(self.path, 'fault')))
        self.locate_led = bool(int(readattr(self.path, 'locate')))
        self.status = readattr(self.path, 'status')

    def __init__(self, enclosure_path, slot_name):
        self.name = slot_name
        self.path = os.path.join(enclosure_path, slot_name)
        self.update()
        self.disk = Disk(os.path.join(enclosure_path, slot_name, 'device'))

    def switch_fault(self):
        self._write_attr('fault', ENABLE_STRING)
        self.update()

    def switch_locate(self):
        self._write_attr('locate', ENABLE_STRING)
        self.update()
 
    def __str__(self):
        return self.name
