"""Design plugin
{i}join
{i}pay"""
from . import jon, pay 

@ItzSjDude(outgoing=True, pattern="join")
async def _(event):
    await jon(event)


@ItzSjDude(outgoing=True, pattern="pay")
async def _(event):
    await pay(event)
