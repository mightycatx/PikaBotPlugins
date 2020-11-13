"""Enables Seen Counter in any message
{I}fwd <reply to msg/media/stickers/docs>"""

from . import _fwd


@ItzSjDude(outgoing=True, pattern="fwd(.*)")
async def _(event):
    await _fwd(event)
