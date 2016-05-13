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

class FlowControl(object):
    """Controlling FlowControl"""
    def __init__(self):
        super(FlowControl, self).__init__()
        self.previousTime = 0
        self.service = 0
        self.total = 0
        self.user = -2

    def _get_user(self):
        us = random.random()
        if us < 0.8:
            user = users[random.randint(0,5)]
            return user
        else:
            return "Anonymous"


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

if __name__ == "__main__":
    fl = FlowControl()

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
    except:
        pass
    finally:
        # GPIO.cleanup()
        pass
