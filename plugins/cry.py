"""Use cmd `{i}lcry` to cry"""

from . import _cry


@ItzSjDude(outgoing=True, pattern="lcry")
async def _(event):
    await _cry(event)
