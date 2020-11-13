"""18+ friendly animations
{i}fuck
{i}kess
{i}sux
"""
from . import _fuck


@ItzSjDude(outgoing=True, pattern=r"(.*)")
async def _(event):
    await _fuck(event)
