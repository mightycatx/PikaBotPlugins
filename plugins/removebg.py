"""**Remove image background***\n
{i}rmbg <reply to image>
{i}rmbg <Image link >"""

from . import _rmbg


@ItzSjDude(outgoing=True, pattern="rmbg ?(.*)")
async def _(event):
    await _rmbg(event)
