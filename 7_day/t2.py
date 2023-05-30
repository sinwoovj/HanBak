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

DEST2TIME_MS = 8000
DETECT_LANGE_MM = 300
DEFAULT_SPEED = 50
H_RANGE = 45 // 2

bot = None
imu = None
lidar = None
botex = None
def init():
    global bot, imu, lidar

    bot = SerBot()
    imu = IMU()
    lidar = Rplidar()
    botex = SerBotEx(bot)

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
        else:
            return False

def stablilizer(yaw):
    pass

def main():

    check_trun = False

    init()

    t0_ms = timeit.default_timer()

    while True:
        t1_ms = timeit.default_timer()
        if (t1_ms - t0_ms) * 1000 >= DEST2TIME_MS:
            if not check_trun:
                t0_ms = timeit.default_timer()
                check_trun = True
                botex.turnAngleLeft(bot,180)
                while(timeit.default_timer() * 1000 <= 18000):
                    bot.forward()
                destroy()
            else:
                break

        yaw = tuple(imu.getGyro().values())[2]
        point_frame = lidar.getVectors()

        stablilizer(yaw)
        detect = forward_detect(point_frame)
    
        print(yaw, detect)

    destroy()

if __name__ == "__main__":
    main()

"""
이 코드는 Serbot, IMU 그리고 LiDAR에서 Rplidar와 같은 필수적인 라이브러리/모듈들을 가져옵니다. 
 DEST2TIME_MS를 5000 밀리초, DETECT_LANGE_MM을 300 밀리미터, DEFAULT_SPEED를 50으로, 
 H_RANGE를 45 // 2 (정수 나누기)로 설정하는 몇 가지 상수를 정의합니다.

그런 다음, 전역 변수 bot, imu 및 lidar를 SerBot, IMU 및 Rplidar 클래스의 각 인스턴스로 초기화합니다. 
 init() 함수는 Rplidar에 연결하고 그 모터를 시작한 뒤 bot의 속도를 DEFAULT_SPEED로 설정하고 앞으로 전진합니다.

destroy() 함수는 로봇과 Rplidar 모터를 멈춥니다.

forward_detect() 함수는 Rplidar의 getVectors() 메서드에서 얻은 point frame을 받아 
 로봇 앞에 장애물이 있는지 확인합니다. 로봇에서 일정 거리와 각도 범위 내에 장애물이 있으면 True를 반환하고 
 그렇지 않으면 False를 반환합니다.

turn_180() 함수는 SerBot 클래스의 메서드를 사용하여 왼쪽으로 로봇을 회전시켜 180도 회전할 때까지 계속합니다.

stabilizer() 함수는 입력 매개변수로 yaw를 사용하지만 현재 아무것도 하지 않습니다.

main() 함수는 먼저 init() 함수를 호출하고 check_turn 변수를 False로 설정합니다. 그런 다음, 
 장애물이 로봇 앞에 있거나 5초가 지날 때까지 계속 실행되는 무한 while 루프에 들어갑니다. 
 루프 내에서 IMU의 getGyro() 메서드로 yaw와 Rplidar의 getVectors() 메서드에서 point_frame을 가져옵니다. 
 그런 후 stabilizer() 함수를 사용하여 로봇을 안정화하고 forward_detect() 함수를 사용하여 
 일정 거리와 각도 범위 내의 장애물이 있는지 확인한 다음 현재 yaw와 검출 상태를 출력합니다. 
 5초 제한 시간이 초과되고 check_turn이 True가 아니면 turn_180() 함수를 호출하고 check_turn을 True로 설정합니다. 
 그렇지 않으면 while 루프를 탈출하고 destroy() 함수를 호출합니다.

if __name__ == "__main__": 문은 이 스크립트가 모듈로 가져오는 것이 아니라 직접 실행될 때만
 main () 함수가 호출되도록 보장합니다.


"""