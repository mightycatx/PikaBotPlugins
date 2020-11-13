# Credit: @r4v4n4
"""fake Leave
{i}fleave"""


@ItzSjDude(outgoing=True, pattern=r"fleave")
async def _(event):
    await _fleave(event)
