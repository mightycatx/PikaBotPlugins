"""ANIMATION PLUGIN
{i}ding"""


@ItzSjDude(outgoing=True, pattern=r"ding")
async def _(event):
    await ding(event)
