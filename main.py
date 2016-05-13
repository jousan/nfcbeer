import time
import RPi.GPIO as GPIO

class FlowControl(object):
    """Controlling FlowControl"""
    def __init__(self):
        super(FlowControl, self).__init__()
        self.previousTime = 0
        self.service = 0
        self.total = 0

    def update(self, channel):
        tim = time.time()
        delta = tim - self.previousTime
        if delta < 500:
            self.hertz = 1000.0 / delta
            self.flow = self.hertz / 450.0  # Liter/Second
            service = self.flow * (delta / 1000.0)
            self.service  += service
            self.total    += service
        else:
            # Guardar a usuari self.service
            self.service = 0
            self.user = self._get_user()

        self.previousTime = tim


if __name__ == "__main__":
    fl = FlowControl()

	GPIO.setmode(GPIO.BCM) # use real GPIO numbering
	GPIO.setup(22,GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(22, GPIO.RISING, callback=fl.update, bouncetime=20)

    try:
        while True:
            time.sleep(1)
    except:
        pass
    finally:
        GPIO.cleanup()
