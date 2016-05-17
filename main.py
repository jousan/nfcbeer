"""
NFCBeer

Usage:
 nfcbeer.py client <id>
 nfcbeer.py server
 nfcbeer.py [-h | --help]

Options:
 -h --help      Shows help
"""
from docopt import docopt
import time
# import RPi.GPIO as GPIO
import random

users = [
    "0001",
    "0002",
    "0003",
    "0004",
    "0005",
    "0006"
]


class FakeNFCReader(object):
    """
    Fake NFC Reader class

    Mimicks an NFC Reader
    """

    uids = [
    "0000000000",
    "1111111111",
    "2222222222",
    "3333333333",
    "4444444444",
    "5555555555",
    "6666666666",
    "7777777777",
    "8888888888",
    "9999999999"
    ]

    def __init__(self):
        self.uid = None

    def is_card_present(self):
        r = random.random()
        if r < 0.8:
            self.uid = self.uids[random.randint(0,9)]
        else:
            self.uid = None
        return self.uid

    def read_uid(self):
        return self.uid


class FlowControl(object):
    """Controlling FlowControl"""
    def __init__(self, nfc=None):
        super(FlowControl, self).__init__()
        self.previousTime = 0
        self.service = 0
        self.total = 0
        self.user = -2
        self.nfc = nfc

    def _get_user(self):
        if self.nfc is not None:
            if self.nfc.is_card_present():
                return self.nfc.read_uid()
        return "None"

    def update(self, channel):
        tim = time.time()
        delta = tim - self.previousTime
        if delta < 0.50:
            print ".",
            self.hertz = 1000.0 / delta
            self.flow = self.hertz / 450.0  # Liter/Second
            service = self.flow * (delta / 1000.0)
            self.service  += service
            self.total    += service
        else:
            if self.user != -2:
                print "+"
                print "user", self.user, " drank ", self.service
            # Guardar a usuari self.service
            self.service = 0
            self.user = self._get_user()

        self.previousTime = tim

    def _debug_dump(self):
        print "DBG: TOTAL: ", self.total, "Servei:", self.service



class BeerControl(object):
    """Control KEG"""
    def __init__(self):
        super(BeerControl, self).__init__()

    def run(self):
        nf = FakeNFCReader()
        fl = FlowControl(nfc=nf)

        # GPIO.setmode(GPIO.BCM) # use real GPIO numbering
        # GPIO.setup(22,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # GPIO.add_event_detect(22, GPIO.RISING, callback=fl.update, bouncetime=20)


        random.seed(1)
        c = 0
        try:
            while True:
                a = random.random()
                if a < 0.3:
                    fl.update(1)

                if a < 0.009:
                    time.sleep(0.550)

                time.sleep(0.002)
                c += 1
                if c > 1000:
                    c = 0
                    fl._debug_dump()
        except Exception as e:
            print e
        finally:
            # GPIO.cleanup()
            pass


if __name__ == "__main__":
    arguments = docopt(doc=__doc__, version="NFCBEER 1.0")
    print arguments
    c = BeerControl()
    c.run()
