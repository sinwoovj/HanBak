from pop import Camera
from pop.Pilot import Object_Follow
from pop.Pilot import SerBot
from lidar import Lidar
from playsound import playsound # 미디어 출력 패키지 >> pip install playsound
import google_cloud_tts # google_cloud_tts.py 파일 
import time

of = None
bot = None
count = 0
serbot_width = 0
direction_count = 0

def setup():
    global bot, of

    cam = Camera()
    of = Object_Follow(cam)
    bot = SerBot()

    serbot_width = 500
    direction_count = 8
    lidar = Lidar(serbot_width, direction_count)
    current_direction = 0
    flag = True

    of.load_model()
    print("="*50)
    print("모델 로딩이 완료되었습니다.")
    print("10초 후 작동이 시작됩니다.")
    google_cloud_tts.google_tts("모델 로딩이 완료되었습니다. 10초 후 작동이 시작됩니다.", "./audio/output1.mp3")
    playsound('./auio/output1.mp3')
    
def loop():
    global count
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
            google_cloud_tts.google_tts("사람을 찾을 수 없습니다.")
            playsound('./auio/output1.mp3')
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
    
    bot.stop()

if __name__ == '__main__':
    main()