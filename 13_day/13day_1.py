from pop import Camera
from pop.Pilot import Object_Follow
from pop.Pilot import SerBot
import time

of = None
bot = SerBot()
count = 0
x = 0

def setup():
    global bot, of

    cam = Camera()
    of = Object_Follow(cam)
    bot = SerBot()

    of.load_model()
    print("="*50)
    print("모델 로딩이 완료되었습니다.")
    print("10초 후 작동 됩니다.")
    
def loop():
    person = of.detect(index='person')
    if person :
        x = round(person['x'] * 4, 1) # * 스케일 Scale
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
        bot.stop()
        print("사람을 찾을 수 없습니다.")
        count += 1
        time.sleep(0.05)

def main():
    setup()
    while True:
        try:
            loop()
        except KeyboardInterrupt:
            break
    
    bot.stop()

if __name__ == '__main__':
    main()