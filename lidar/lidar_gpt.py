from pop.Pilot import SerBot
from lidar import Lidar
import random

def main():
    serbot_width = 500
    direction_count = 8
    speed = 50

    bot = SerBot()
    lidar = Lidar(serbot_width, direction_count)
    current_direction = 0
    flag = True
    
    print("Start SerBot!!!")

    while flag:
        try:
            if lidar.collisonDetect(300)[current_direction]:
                bot.stop()
                continue

            detect = lidar.collisonDetect(800)

            if sum(detect) == direction_count:
                bot.stop()
                continue
            
            if detect[current_direction]:
                open_directions = [i for i, val in enumerate(detect) if not val]
                current_direction = random.choice(open_directions)

            if current_direction == 0:
                bot.forward(speed)
            elif current_direction == 1 or current_direction == 2:
                bot.turnLeft(speed)
            elif current_direction == 6 or current_direction == 7:
                bot.turnRight(speed)
            print(detect)

        except (KeyboardInterrupt, SystemError):
            flag = False
    
    bot.stop()
    print('Stopped Serbot!')

if __name__ == '__main__':
    main()
