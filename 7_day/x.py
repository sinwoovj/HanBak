from pop.Pilot import SerBot
from pop.Pilot import IMU
from pop.LiDAR import Rplidar
import time
import timeit

bot = None
imu = None
lidar = None
DEST2DISTANCE = 5000 # 5meters 
DETECT_DISTANCE = 300 # Obstacle detection distance
STABILIZER_THRESHOLD = 5
KP = 1.2
KI = 0.002

def init():
    global bot, imu, lidar
    
    bot = SerBot()
    imu = IMU()

    bot.setSpeed(50)
    bot.forward()

    lidar = Rplidar()
    lidar.connect()
    lidar.startMotor()
    
    # Add the following line
    bot.stop()

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

def turn_around():
    bot.turn(180)

def avoid_obstacle():
    bot.turn(90)

def pidController(current_yaw, target_yaw):
    error = target_yaw - current_yaw
    steerAngle = error * KP
    left_speed = bot.speed + error * KP + (error - STABILIZER_THRESHOLD) * KI
    right_speed = bot.speed - error * KP - (error - STABILIZER_THRESHOLD) * KI
    bot.setSpeed(left_speed)
    bot.setSpeed(right_speed)

def main():
    init()

    t0_ms = 0
    CHECK_TURN = False
    DEST2TIME = DEST2DISTANCE // bot.speed * 60 * 1000 # 시간(ms) = 거리(mm) / 속도(mm/s) * 60 * 1000

    target_yaw = tuple(imu.getGyro().values())[2]
    point_frame = lidar.getVectors()

    while True:
        current_yaw = tuple(imu.getGyro().values())[2]
        pidController(current_yaw, target_yaw)
        detect = forward_detect(point_frame, DETECT_DISTANCE)

        if detect:
            avoid_obstacle()
            point_frame = lidar.getVectors()
        else:
            left_distance = get_distance('left')
            right_distance = get_distance('right')

            if left_distance + right_distance >= DEST2DISTANCE:
                if not CHECK_TURN:
                    CHECK_TURN = True
                    turn_around()
                    t0_ms = timeit.default_timer()
                else:
                    break

            if CHECK_TURN and (timeit.default_timer() - t0_ms) * 1000 >= DEST2TIME:
                break

            print(left_distance, right_distance)

    destroy()

def get_distance(self, direction):
        if not self._sonar:
            raise RuntimeError('Sonar sensor is not available')

        return self._sonar.distance(direction) * 1000

if __name__ == "__main__":
    main()

"""
Serbot을 사용하여 IMU 및 Lidar 기반으로 하는 정적 경로 주행 코드입니다. 

이 코드는 IMU를 사용하여 최대한 직진성을 유지하면서 5M 직진, 180도 회전 한 후 다시 5M 직진하는 동안 

Lidar를 사용하여 충돌 감지가 있을 시 장애물을 피하고 다시 주행하는 방식입니다.

위 코드에서는 `init()` 함수에서 Serbot 및 IMU, Lidar 초기화를 진행합니다. 

`destroy()` 함수에서는 Serbot 및 Lidar 정지를 담당합니다.

`pidController()` 함수에서는 현재 yaw 값과 목표 yaw 값을 비교하여 PID 알고리즘을 사용하여 
좌우 바퀴의 속도를 제어하여 최대한 직진성을 유지합니다.

`forward_detect()` 함수에서는 Lidar에서 수집한 데이터로부터 전방에 장애물이 검출되었는지 확인합니다.

`avoid_obstacle()` 함수에서는 Lidar에서 전방 장애물을 감지했을 경우 90도 회전하도록 합니다.

마지막으로 `main()` 함수에서는 정적 경로 주행을 위한 조건문들을 구성합니다. 

먼저, `detect` 변수가 True인 경우 `avoid_obstacle()` 함수를 호출하고 다시 Lidar 데이터를 가져옵니다. 

그렇지 않으면 `pidController()` 함수를 호출하여 직진성을 유지하면서 전진하며, 
`left_distance` 와 `right_distance` 의 합이 5미터가 되면 180도 회전해야 한다는 것을 체크하도록 합니다. 

이미 회전했다면 이제 코드를 종료합니다. 예상 시간(`DEST2TIME`)내에 회전하지 못했다면 코드를 종료합니다. 

마지막으로 거리와 관련된 정보를 프린트하도록 합니다.
"""
