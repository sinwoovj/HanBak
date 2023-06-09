from pop import Camera
from pop.Pilot import Object_Follow
from pop.Pilot import SerBot
from pop.Pilot import IMU
from pop.LiDAR import Rplidar
import timeit

of = None
bot = None
count = 0
serbot_width = 0
direction_count = 0
imu = None
lidar = None
DETECT = 300

def setup():
    global bot, of, imu, lidar

    cam = Camera()
    of = Object_Follow(cam)
    bot = SerBot()

    imu = IMU()
    lidar = Rplidar()

    lidar.connect()
    lidar.startMotor()

    of.load_model()
    print("="*50)
    print("모델 로딩이 완료되었습니다.")
    print("10초 후 작동이 시작됩니다.")

def destroy():
    bot.stop()
    lidar.stopMotor()

def forward_detect(point_frame, dest):
    for p in point_frame:
        if p[0] > (360-30) or p[0] < (0+30):
            if p[1] <= dest:
                return True
        else:
            return False

def loop():
    global count

    point_frame = lidar.getVectors()
    detect = forward_detect(point_frame, DETECT)
    yaw = tuple(imu.getGyro().values())[2]
    print(yaw, detect)
    if(detect):
        bot.stop()

    person = of.detect(index='person')
    if person :
        count = 0
        x = round(person['x'] * 4, 1) # * 스케일 Scale
        rate = round(person['size_rate'], 1)

        if rate < 0.1 :
            bot.setSpeed(90)
        elif rate < 0.15 :
            bot.setSpeed(80)
        elif rate < 0.3 :
            bot.stop()
        else:
            bot.forward(60)
            bot.steering = 1.0 if x > 1.0 else -1.0 if x < -1.0 else x
        
        print(f"rate : {rate}, steering : {bot.steering}")
        
    else:
        if count > 40 :
            bot.stop()
            print("사람을 찾을 수 없습니다.")
        elif count == 20:
            bot.setSpeed(50)
            if bot.steering < 0:
                bot.turnLeft()
            else:
                bot.turnRight()
            cnt += 1
        else: 
            count += 1


def main():
    setup()
    while True:
        try:
            loop()
        except KeyboardInterrupt:
            break
    
    destroy()

if __name__ == '__main__':
    main()