@ItzSjDude(outgoing=True, pattern="chain(.*)")
async def _(event):
    await _chain(event)
