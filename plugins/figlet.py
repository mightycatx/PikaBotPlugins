"""Figlet Module
{i}figlet <font name>
"""
from . import _figlet

@ItzSjDude(outgoing=True, pattern=r"figlet ?(.*)")
async def _(event):
    await _figlet(event)
