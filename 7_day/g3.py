import random
from pop.Pilot import SerBot
from pop.Pilot import IMU
from pop.LiDAR import Rplidar
import time

# SerBot 초기화
bot = SerBot()
imu = IMU()
lidar = Rplidar()

# IMU, Lidar 초기화
# imu.start() # IMU 클래스 내부에서 필요한 초기화 과정 실행
lidar.connect() # lidar 객체를 연결

def detect_obstacle():
    distance = lidar.get_distance()

    if distance < 50:
        avoid_obstacle()

def avoid_obstacle():
    bot.move_backward(30)

    if random.randint(0, 1) == 0:
        bot.rotate(imu.heading + 90)
    else:
        bot.rotate(imu.heading - 90)

    bot.move_forward(30)
    bot.rotate(imu.heading)

def straight_5m():
    imu_heading = imu.heading
    start_position = bot.get_position()
    
    while True:
        current_position = bot.get_position()
        distance_traveled = current_position - start_position

        if distance_traveled >= 500:
            break

        bot.rotate(imu_heading)
        detect_obstacle()

def turn_180_degrees():
    imu_heading = imu.heading
    start_heading = imu_heading
    
    while True:
        current_heading = imu.heading
        degrees_turned = abs(current_heading - start_heading)

        if degrees_turned >= 180:
            break

        bot.rotate(imu_heading + 180)
        detect_obstacle()

# 메인 함수
def main():
    straight_5m()
    turn_180_degrees()
    straight_5m()

if __name__ == "__main__":
    main()
