""" Get the Bots in any chat*
Syntax: {i}gbot"""

from . import _gbot


@ItzSjDude(outgoing=True, pattern="gbot(.*)")
async def _(event):
    await _gbot(event)
