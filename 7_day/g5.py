from pop.Pilot import SerBot
from pop.Pilot import IMU
from pop.LiDAR import Rplidar
import timeit
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
            w = 0.73
        elif speed <= 1000:
            w = 0.76
        return n/ 90 - (n/90) * w
    
    def turn_(self,a):
        d = self.__calc_delay(a)
        self.turnLeft()
        time.sleep(d)
        self.stop()
        
DEST2TIME_MS = 13000
DETECT_LANGE_MM = 300
DEFAULT_SPEED = 60
H_RANGE = 45 // 2
ANGLE = 215

bot = None
imu = None
lidar = None
botex = None

def init():
    global bot, imu, lidar, botex
    
    bot = SerBot()
    imu = IMU()
    lidar = Rplidar()
    botex = SerBotEx()

    lidar.connect()
    lidar.startMotor()

    bot.setSpeed(DEFAULT_SPEED)
    bot.forward()

def destroy():
    bot.stop()
    lidar.stopMotor()

def forward_detect(point_frame):
    for p in point_frame:
        if p[0] > (360-H_RANGE) or p[0] < (0+H_RANGE):
            if p[1] <= DETECT_LANGE_MM:
                return True
    return False

def stabilizer(yaw):
    pass

def main():
    check_turn = False

    init()

    t0_ms = timeit.default_timer()

    while True:
        t1_ms = timeit.default_timer()
        while (t1_ms - t0_ms) * 1000 <= DEST2TIME_MS:
            t1_ms = timeit.default_timer()
            print(t1_ms - t0_ms)
            
        t0_ms = timeit.default_timer()
        botex.turn_(ANGLE)
        bot.forward()
        
        # yaw = tuple(imu.getGyro().values())[2]
        # point_frame = lidar.getVectors()

        # stabilizer(yaw)
        # detect = forward_detect(point_frame)
    
        #print(yaw, detect)

        t0_ms = timeit.default_timer()

        while (t1_ms - t0_ms) * 1000 <= DEST2TIME_MS:
            t1_ms = timeit.default_timer()
            print(t1_ms - t0_ms)
        botex.turn_(ANGLE)
        destroy()

        print("finish")
        break

if __name__ == "__main__":
    main()