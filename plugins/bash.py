"""For executing linux/Gnu Commands
{i}bash <cmd> """

from . import _bash, bot, bot2, bot3, bot4


@ItzSjDude(pattern="bash ?(.*)")
async def _(event):
    await _bash(event)
