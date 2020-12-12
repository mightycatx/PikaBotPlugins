"""**Get Detailed info about any message**\n
{i}json <reply to msg>"""


@ItzSjDude(outgoing=True, pattern="json")
async def _(event):
    await _json(event)
