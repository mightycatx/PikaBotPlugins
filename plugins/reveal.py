""" Plugin for reading nd Exporting as messge on Tg
{i}reveal <reply to file>
"""
# Made By @ItzSjDude. All rights reserved

from . import _reveal


@ItzSjDude(pattern=r"reveal")
async def _(event):
    await _reveal(event)
