from math import sqrt

def get_Percentage(Max, Value):
    fraction = float(Value) / Max
    return fraction

def get_Distance(v1, v2):
    x = v1[0] - v2[0]
    y = v1[1] - v2[1]
    return sqrt(x**2 + y**2)

class Timer(object):
    """ A timer to give callbacks over periods of time.

        This allows for continuous updates of the game.
    """

    def __init__(self, interval , callback, onetimer = False):
        """Interval: the amount of milliseconds between timers.
           Callback: callable when the timer/interval expires.
           Onetimer: True for a timer that only acts once.
        """
        self.interval = interval
        self.callback = callback
        self.onetimer = onetimer
        self.time = 0
        self.alive = True

    def update(self, time_passed):
        if not self.alive:
            return

        self.time += time_passed
        if self.time > self.interval:
            self.time -= self.interval
            self.callback()

            if self.onetimer:
                self.alive = False
