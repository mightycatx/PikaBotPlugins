"""For executing linux/Gnu Commands
{i}bash <cmd> """

from . import _bash


@ItzSjDude(pattern="bash ?(.*)")
async def _(event):
    await _bash(event)
