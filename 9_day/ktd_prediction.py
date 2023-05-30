from pop.Pilot import SerBot
from pop.Pilot import IMU
from pop.AI import Linear_Regression
import time

bot = SerBot()
imu = IMU()
linear = Linear_Regression(True, ckpt_name='ktd')

bot.forward()
bot.setSpeed(80)

try:
    while True: 
        gz = imu.getGyro('z')
        pred_steer = round(linear.run([gz])[0][0], 1)
        pred_steer = -pred_steer #Is this correct ???   
        
        """
        You need to calculate a reasonable 'pred_steer' to put in here. 
        ex) (pred_steer+0.1) * 1.5
        """
        
        bot.steering = 1.0 if pred_steer > 1.0 else -1.0 if pred_steer < -1.0 else pred_steer 
        
        time.sleep(0.1)
except KeyboardInterrupt:
    bot.stop()