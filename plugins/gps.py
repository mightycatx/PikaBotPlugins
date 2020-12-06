"""**GPS**\n\n
{i}gps <location name>\n
USAGE: Sends you the given location name"""

from . import _gps
@ItzSjDude(outgoing=True, pattern="gps ?(.*)")
async def _(event):
     await _gps(event)
