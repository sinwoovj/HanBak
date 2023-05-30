import random
from pop.Pilot import SerBot
from pop.Pilot import IMU
from pop.LiDAR import Rplidar
import time
import timeit

# SerBot 초기화
bot = SerBot()
imu = IMU()
lidar = Rplidar()

# IMU, Lidar 초기화
imu_sensor = imu.IMU()
lidar_sensor = lidar.Lidar()

def detect_obstacle():
    # Lidar로 거리 측정
    distance = lidar_sensor.measure_distance()
    
    if distance < 50:
        # 거리가 50cm 이하일 경우 장애물이 있음
        # 회피 알고리즘 실행
        avoid_obstacle()

def avoid_obstacle():
    # robot을 일정 거리만큼 후진시킴
    bot.move_backward(30)
    
    # 임의로 왼쪽 또는 오른쪽으로 회전함
    if random.randint(0, 1) == 0:
        bot.rotate(imu_sensor.get_heading() + 90)
    else:
        bot.rotate(imu_sensor.get_heading() - 90)
        
    # 후진한 거리만큼 다시 직진함
    bot.move_forward(30)
    
    # 다시 원래 heading 방향으로 회전함
    bot.rotate(imu_sensor.get_heading())

    
def straight_5m():
    imu_heading = imu_sensor.get_heading() # IMU에서 현재 heading 값 읽음
    start_position = bot.get_position()
    while True:
        current_position = bot.get_position()
        distance_traveled = current_position - start_position
        
        # 거리가 5m 이상일 때까지 직진
        if distance_traveled >= 500:
            break
        
        # robot을 일정한 heading으로 유지
        bot.rotate(imu_heading)
        
        # 장애물 검출 함수 호출
        detect_obstacle()

def turn_180_degrees():
    imu_heading = imu_sensor.get_heading() # IMU에서 현재 heading 값 읽음
    start_heading = imu_heading
    
    while True:
        current_heading = imu_sensor.get_heading()
        degrees_turned = abs(current_heading - start_heading)
        
        # 180도 회전할 때까지 회전
        if degrees_turned >= 180:
            break
        
        # robot의 방향을 180도 회전시킴
        bot.rotate(imu_heading + 180)
        
        # 장애물 검출 함수 호출
        detect_obstacle()

# 코드 실행
straight_5m()
turn_180_degrees()
straight_5m()
