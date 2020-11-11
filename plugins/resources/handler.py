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
   pika_id1 = 1111
if bot2 is not None:
   pika_id2 = i2
else:
   pika_id2 = 1011
if bot3 is not None:
   pika_id3 = i3
else:
   pika_id3 = 1010
if bot4 is not None:
   pika_id4 = i4
else:
   pika_id4 = 1001

async def pikaa(event, shortname):
    pika_pi = await event.client.get_me()
    AS = os.environ.get(f"{shortname}", None).split('|')
    erx = "[Error?](https://t.me/c/1464516488/2)"
    try:
       if pika_id1 == pika_pi.id:
           a=AS[0]
           if a is not None and shortname.startswith("ALIVE"): 
               return a
           if a is None and shortname.startswith("ALIVE"):
               return er
           if not shortname.startswith("ALIVE"):
               return a
       if pika_id2 == pika_pi.id:
           a=AS[1]
           if a is not None and shortname.startswith("ALIVE"): 
               return a
           if a is None and shortname.startswith("ALIVE"):
               return er
           if not shortname.startswith("ALIVE"):
               return a
   
       if pika_id3 == pika_pi.id:
           a=AS[2]
           if a is not None and shortname.startswith("ALIVE"): 
               return a
           if a is None and shortname.startswith("ALIVE"):
               return er
           if not shortname.startswith("ALIVE"):
               return a

       if pika_id4 == pika_pi.id:
           a=AS[3]
           if a is not None and shortname.startswith("ALIVE"): 
               return a
           if a is None and shortname.startswith("ALIVE"):
               return er
           if not shortname.startswith("ALIVE"):
               return a
       else:  
          pass
    except BaseException:
        pass

def pikarestart():
    pika.restart()
