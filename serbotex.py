from pop.Pilot import SerBot
import time
class SerBotEx(SerBot):
    def __calc_delay(self, n):
        speed = self.getSpeed()
        if speed <= 20:
            w = 0.0
        elif speed <= 40:
            w = 0.4
        elif speed <= 60:
            w = 0.6
        elif speed <= 80:
            w = 0.7
        elif speed <= 1000:
            w = 0.76
        return n/ 90 - (n/90) * w
    def turnAngleLeft(self, n):
        d = self.__calc_delay(n)
        self.turnLeft()
        time.sleep(d)
        self.stop()

    def turnAngleRight(self, n):
        d = self.__calc_delay(n)
        self.turnRight()
        time.sleep(d)
        self.stop()