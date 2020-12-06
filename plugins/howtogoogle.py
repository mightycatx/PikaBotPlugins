# Modded from dagd.py
"""
Animate How To Google\n\n
{i}ggl <query>

"""
By @loxxi
from . import _ggl 

@ItzSjDude(outgoing=True, pattern="ggl(.*)")
async def _(event):
    await _ggl(event) 
