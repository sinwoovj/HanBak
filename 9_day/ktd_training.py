from pop.Pilot import SerBot
from pop.Pilot import IMU
from pop.AI import Linear_Regression
import numpy as np
import time

bot = SerBot()
imu = IMU()
linear = Linear_Regression(ckpt_name='ktd')

dataset = {'gyro_z':[], 'steer':[]}
bot.setSpeed(80)

for n in np.arange(-1.0, 1.0+0.1, 0.2):
    n = round(n, 1)
    bot.steering = n
 
    bot.forward()
    time.sleep(0.5)   
    gy = imu.getGyro('z')
    time.sleep(0.5)
    
    bot.backward()
    time.sleep(1)
    bot.stop()

    dataset['gyro_z'].append([gy])
    dataset['steer'].append([n]) 
    print({'gyro_z':gy, 'steer':n}) 

linear.X_data = dataset['gyro_z']
linear.Y_data = dataset['steer']

linear.train(times=100, print_every=10)