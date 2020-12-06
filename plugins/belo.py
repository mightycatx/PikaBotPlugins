"""
Say something interesting...
{i}belo
"""
from . import belo


@ItzSjDude(outgoing=True, pattern=r"belo")
async def _(event):
    await belo(event)
