#%%
import time
from pop.Pilot import SerBot
#%%
bot = SerBot()
bot.setSpeed(50)
bot.move(-60,50)
time.sleep(2)
bot.move(60,50)
time.sleep(6)
bot.move(180,50)
time.sleep(6)
bot.move(-60,50)
time.sleep(4)
bot.move(0,50)
time.sleep(4)
bot.move(120,50)
time.sleep(6)
bot.move(-120,50)
time.sleep(6)
bot.move(0,50)
time.sleep(2)
bot.stop()

# %%
