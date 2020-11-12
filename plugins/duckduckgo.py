"""use command {i}ducduckgo"""


@ItzSjDude(outgoing=True, pattern="ducduckgo (.*)")
async def _(event):
    await ducgo(event)
