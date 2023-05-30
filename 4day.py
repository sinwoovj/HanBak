from pop.LiDAR import Rplidar
from pop.Pilot import SerBot
from serbotex import SerBotEx

import time

lidar = Rplidar()
bot = SerBotEx()
lidar.connect()
lidar.startMotor()
bot.setSpeed(30)
bot.forward()

while True:
    V = lidar.getVectors()
    for item in V:
        # if item[0] >= 330 or item[0] < 30:
        print("Angle: %.1f, Dist: %d"%(item[0], item[1]))
        if item[1] < 400:
            bot.stop()
            bot.turnAngleLeft(10)
            time.sleep(0.5)
            bot.forward()