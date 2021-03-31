"""Globally bans User
{i}gban <userid/username/mention> <Reason>
"""
from . import gban


@ItzSjDude(pattern="gban(?: |$)(.*)")
async def _(event):
    await gban(event)
