# Modded from dagd.py
"""
Animate How To Google\n\n
{i}ggl <query>

"""
from . import _ggl

# By @ loxxi


@ItzSjDude(outgoing=True, pattern="ggl(.*)")
async def _(event):
    await _ggl(event)
