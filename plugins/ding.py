"""ANIMATION PLUGIN
{i}ding"""
from . import _ding

@ItzSjDude(outgoing=True, pattern=r"ding")
async def _(event):
    await _ding(event)
