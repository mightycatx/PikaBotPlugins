import os
from plugins.heroku import *
try:
    from pikabot import bot, bot2, bot3, bot4
    i1 = bot.uid
    i2 = bot2.uid
    i3 = bot3.uid
    i4 = bot4.uid

except BaseException:
    pass

if bot is not None:
   pika_id1 = i1
else:
   pika_id1 = 0110
if bot2 is not None:
   pika_id2 = i2
else:
   pika_id2 = 0101
if bot3 is not None:
   pika_id3 = i3
else:
   pika_id3 = 1010
if bot4 is not None:
   pika_id4 = i4
else:
   pika_id4 = 1001

def pikaa(a, shortname):
    try:
        AS = os.environ.get(f"{shortname}", None).split('|')
        if a.sender_id == i1:
            return AS[0]
        if a.sender_id == i2:
            return AS[1]
        if a.sender_id == i3:
            return AS[2]
        if a.sender_id == i4:
            return AS[3]
        else:
            pass
    except BaseException:
        pass


def pikarestart():
    pika.restart()
