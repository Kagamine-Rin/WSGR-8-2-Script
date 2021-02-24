from os import system
import core

bot = core.bot(offs=120)
system('adb devices')
bot.loop()