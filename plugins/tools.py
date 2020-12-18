"""Telegraph and Other Utilities
Available Commands:
{i}app <appname>
{i}tm <as reply to a media>
{i}tt <as reply to a large text>
"""
from . import apk, _invite, _telegraph

@ItzSjDude(outgoing=True, pattern="app (.*)")
async def _(e)
    await apk(e)

@ItzSjDude(outgoing=True, pattern="invite ?(.*)")
async def _(event):
    await _invite(event)

@ItzSjDude(outgoing=True, pattern="t(m|t) ?(.*)")
async def _(event):
    await _telegraph(event)

