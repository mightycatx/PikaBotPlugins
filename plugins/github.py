"""**Get information about an user on GitHub**/n
{i}github <username>"""
from . import _github 

@ItzSjDude(outgoing=True, pattern="github (.*)")
async def _(event):
    await _github(event)
