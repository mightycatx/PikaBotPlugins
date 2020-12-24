"""Quickly make a decision
{i}decide"""

from . import decide 
@ItzSjDude(outgoing=True, pattern="decide")
async def _(event):
    await decide(event)
