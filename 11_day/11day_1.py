# 모델 테스트용
from pop import Camera
from pop.Pilot import Object_Follow
import time

cam = Camera()
of = Object_Follow(cam)

of.load_model() 
print("="*50)
print("Model load OK!")
print("It starts in about 10 seconds.")

while True:
    person = of.detect(index='person')
    if person :
        x = round(person['x'], 1)
        rate = round(person['size_rate'], 1)
        print(x, rate)
    time.sleep(0.5)