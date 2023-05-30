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
count = None

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

def stabilizer(yaw, t0_1):
    t1_1 = timeit.default_timer()
    if (t1_1-t0_1)* 10000>= 100:
        t0_1 = t1_1
        count += 1
        if yaw:
            bot.steering = -1.0
            delay = True
            t0_1 = timeit.default_timer()
        
    if (delay):
        t1_1 = timeit.default_timer()
        if(t1_1-t0_1) * 10000 >= 10:
            delay = False
            bot.steering =0.0

def main():
    check_turn = False

    init()

    t0_ms = timeit.default_timer()

    while True:
        count = 0
        t1_ms = timeit.default_timer()
        while (t1_ms - t0_ms) * 1000 <= DEST2TIME_MS:
            t1_ms = timeit.default_timer()
            print(t1_ms - t0_ms)
            
        t0_ms = timeit.default_timer()
        botex.turn_(ANGLE)
        bot.forward()
        
        yaw = tuple(imu.getGyro().values())[2]
        point_frame = lidar.getVectors()

        stabilizer(yaw,t0_ms)
        detect = forward_detect(point_frame)
    
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


"""
==========================================

    t1_1 = timeit.default_timer()
    if (t1_1-t0_1)* 10000>= 100:
        t0_1 = t1_1
        count += 1
        if tuple(IMU.getGyro().values())[2]:
            bot.steering = -1.0
            delay = True
            t0_1 = timeit.default_timer()
        
    if (delay):
        t1_1 = timeit.default_timer()
        if(t1_1-t0_1) * 10000 >= 10:
            delay = False
            bot.steering =0.0
            
    if count > 300:
        break;

==========================================

이 코드는 다양한 요인에 따라 작업을 수행하는 조건부 루프입니다:


timeit.default_timer()는 현재 시스템 시간을 초 단위로 반환하는 Python 함수입니다.

t1_1 = timeit.default_timer()는 t1_1이라는 변수에 현재 시간을 할당합니다.

(t1_1-t0_1)* 10000>= 100은 t1_1과 t0_1 사이의 차이(이전 루프의 지속 시간이어야 함)에 10000을 곱한 값이 100보다 
크거나 같은지 확인합니다. 이 조건이 참이면 이 if-block 내의 코드가 실행됩니다:

t0_1 = t1_1은 기준 시간을 현재 시간으로 업데이트합니다.

count += 1은 카운터 변수를 증가시킵니다.

---------------

tuple(IMU.getGyro().values()[2]는 자이로스코프 판독값이 포함된 tuple에서 세 번째 값을 검색합니다. 
이 값이 0이 아닌 경우 다음 작업이 수행됩니다:

bot.steering = -1.0은 특정 로봇 또는 차량의 조향을 -1.0(왼쪽으로 돌리는 것이 좋습니다)으로 설정합니다.

delay = True는 루프가 완료된 후 지연이 발생해야 함을 나타내는 플래그를 설정합니다.

t0_1 = timeit.default_timer()는 기준 시간을 다시 업데이트합니다.

---------------

if (delay): 지연 플래그가 설정되었는지 확인합니다. 이 경우 다음 작업이 수행됩니다:

t1_1 = timeit.default_timer()는 현재 시간을 다시 가져옵니다.

if(t1_1-t0_1) * 10000 >= 10: 지연 플래그에 10000을 곱한 이후의 지속 시간이 10보다 크거나 같은지 확인합니다. 

이 경우 다음 작업이 수행됩니다:

delay = False는 지연 플래그를 재설정합니다.

bot.timeout = 0.0은 차량의 조향을 0으로 설정하여 정지시킬 수 있습니다.

if count > 300: 루프가 300회 이상 실행되었는지 확인합니다. 그렇다면 루프가 끊어지고 코드는 다음에 오는 것으로 이동합니다.

전반적으로 이 코드는 자이로스코프의 데이터를 기반으로 차량의 스티어링을 제어하는 것으로 보이며, 
방향을 원활하게 변경할 수 있도록 일종의 지연 메커니즘이 설정되어 있습니다.
"""