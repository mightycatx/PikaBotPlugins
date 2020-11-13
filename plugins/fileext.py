"""Get info about a File Extension
{i}filext <extension>"""

from . import _getfilext

@ItzSjDude(outgoing=True, pattern="filext (.*)")
async def _(event):
    await _getfilext(event)
