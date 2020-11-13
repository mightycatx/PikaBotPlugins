"""Prints F with given word
{i}text"""

from . import _ftext


@ItzSjDude(outgoing=True, pattern="ftext ?(.*)")
async def _(event):
    await _ftext(event)
