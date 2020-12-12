"""**pastebin like site**\n
'paste <reply to file/msg>"""

@ItzSjDude(outgoing=True, pattern="paste ?(.*)")
async def _(event):
    await _deldog(event)
