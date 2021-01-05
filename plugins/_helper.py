from . import helper, pika_sudo

if bot: 
   @bot.on(pika_sudo(from_client=1, pattern=r"help ?(.*)"))
if bot2: 
   @bot2.on(pika_sudo(from_client=2, pattern=r"help ?(.*)"))
if bot3: 
   @bot3.on(pika_sudo(from_client=3, pattern=r"help ?(.*)"))
if bot4: 
   @bot4.on(pika_sudo(from_client=4, pattern=r"help ?(.*)"))
@ItzSjDude(outgoing=True, pattern=r"help ?(.*)")
async def _(event):
    await helper(event)
