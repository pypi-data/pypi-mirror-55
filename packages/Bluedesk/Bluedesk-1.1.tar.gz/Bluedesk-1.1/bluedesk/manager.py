from bluepy.btle import Scanner, Peripheral, ADDR_TYPE_RANDOM, DefaultDelegate, ScanEntry

from .config import Config
from .desks import factory, DefaultDesk

class DeskManager:

    MAX_CONNECTION_ATTEMPTS = 5

    def __init__(self):
        self._scanner = Scanner()
        self._peripheral = Peripheral()
        self._desk = None
        self.config = Config()

    def scan_devices(self) -> [ScanEntry]:
        scan_entries = self._scanner.scan()

        return [ entry for entry in scan_entries ]

    def connect(self, device_addr):

        while range(self.MAX_CONNECTION_ATTEMPTS):
            try:
                self._peripheral.connect(device_addr, ADDR_TYPE_RANDOM)
            except:
                continue
            else:
                break

        self._desk = factory(self._peripheral, device_addr)

        if self._desk is None:
            self._peripheral.disconnect()
            raise Exception("Device is not supported")

    @property
    def is_connected(self):
        return self.desk.position is not None if self.desk is not None else False

    @property
    def desk(self) -> DefaultDesk:
        return self._desk