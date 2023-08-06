import teensytoany
class TeensyPower():
    def __init__(self):
        self._teensy = teensytoany.TeensyToAny()
        self._teensy.gpio_pin_mode(13, 'OUTPUT')
        self.poweroff()

    def poweron(self):
        self._teensy.gpio_digital_write(13, 1)

    def poweroff(self):
        self._teensy.gpio_digital_write(13, 0)
