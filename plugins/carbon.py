# Ported by @R4v4n4 from paperplane

"""Carbon Module for PikaBot
{i}carbon <reply to message>"""

from . import _carbon 
@ItzSjDude(outgoing=True, pattern="carbon")
async def _(e):
    await _carbon(e)
