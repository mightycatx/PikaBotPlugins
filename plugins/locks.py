"""**GROUP LOCKS**\n
{i}lock/unlock <all (or) type(s)> 
Usage: Allows you to lock/unlock some common message types in the chat\n
[NOTE: Requires proper admin rights in the chat !!]\n\n 
Available message types to lock/unlock are: 
`all, msg, media, sticker, gif, game, inline, poll, invite, pin, info`
"""

from . import _locks, _rmlocks

@ItzSjDude(outgoing=True, pattern=r"lock ?(.*)")
async def _(event)
    await _locks(event)

@ItzSjDude(outgoing=True, pattern=r"unlock ?(.*)")
async def _(event):
    await _rmlocks(event)
