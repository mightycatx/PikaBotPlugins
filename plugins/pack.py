"""Transforms Msg into file
{i}pack <reply to msg filename.extension>

"""
# Made by @ItzSjDude. All Rights reserved

from . import _pack 

@ItzSjDude(pattern="pack ?(.*)")
async def _(event):
     await _pack(event)
