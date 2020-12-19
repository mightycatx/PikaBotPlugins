"""
{i}color <color_code>
**Usage**: Get color by its color code
"""
# credits @Uniborg

from . import findcolour


@ItzSjDude(outgoing=True, pattern="color (.*)")
async def _(event):
    await findcolour(event)
