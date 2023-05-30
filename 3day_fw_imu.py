import timeit
from pop.Pilot import SerBot, IMU
bot = SerBot()

#%%
bot.setSpeed(60)
bot.forward()
count = 0
t0_1 = timeit.default_timer()

while True:
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
bot.stop()
# %%
bot.stop()
