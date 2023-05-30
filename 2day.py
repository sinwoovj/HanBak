#%%
# "#%%"으로 vscode에서 자체적으로 셀을 분리할 수 있다.
from serbotex import SerBotEx
import time
#%%
bot = SerBotEx()
#%%
bot.setSpeed(50)

#%%

bot.turnAngleLeft(60)
bot.forward()
time.sleep(1)
bot.turnAngleRight(90)
bot.forward()
time.sleep(3)
bot.turnAngleRight(90)
bot.forward()
time.sleep(3)
bot.turnAngleLeft(240)
bot.forward()
time.sleep(2)
bot.turnAngleRight(60)
bot.forward()
time.sleep(2)
bot.turnAngleRight(120)
bot.forward()
time.sleep(3)
bot.turnAngleLeft(240)
bot.forward()
time.sleep(3)
bot.turnAngleRight(120)
bot.forward()
time.sleep(1)
bot.stop()


# %%
bot.stop()
# %%
