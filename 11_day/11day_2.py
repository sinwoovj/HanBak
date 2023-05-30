from pop import Camera
from pop.Pilot import Object_Follow
from pop.Pilot import SerBot
import time

cam = Camera()
of = Object_Follow(cam)
bot = SerBot()

of.load_model() 
print("="*50)
print("모델 로딩이 완료되었습니다.")
print("10초 후 작동 됩니다.")
count = 0
x = 0
while True:
    person = of.detect(index='person')
    if person :
        x = round(person['x'] * 3.5, 1) # * 스케일 Scale
        rate = round(person['size_rate'], 1)
        print("x: "+ str(x)+ ", rate: " + str(rate))
        bot.forward(50)
        bot.steering = 1.0 if x > 1.0 else -1.0 if x < -1.0 else x
        count=0
        if rate < 0.2: # 바운더리 boundary
            print("너무 가까이 있는 것 같습니다.")
            if x > 0 : # 오른쪽 (서보기준)
                bot.turnRight()
                print("오른쪽으로 회전중입니다...")
            elif x < 0 : # 왼쪽 (서보기준)
                bot.turnLeft()
                print("왼쪽으로 회전중입니다...")
            bot.stop()
            time.sleep(0.05)
    else:
        print("사람을 찾을 수 없습니다.")
        # 못찾을경우 처리
        if x > 0 : # 오른쪽 (서보기준)
            bot.turnRight()
            print("사람을 찾지 못해 오른쪽으로 회전중입니다...")
        elif x < 0 : # 왼쪽 (서보기준)
            bot.turnLeft()
            print("사람을 찾지 못해 왼쪽으로 회전중입니다...")
        # count가 50 이상이 될 때까지 찾지 못하면 자동으로 꺼짐
        if(count > 300):
            print("시간이 초과되었습니다. 서보를 종료합니다.")
            bot.stop()
            break
        count += 1
        bot.stop()
        time.sleep(0.05)