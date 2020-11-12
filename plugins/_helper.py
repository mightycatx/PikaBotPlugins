from . import helper


@ItzSjDude(outgoing=True, pattern=r"help ?(.*)")
async def _(event):
    await helper(event)
