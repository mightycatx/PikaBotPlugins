"""
Files Batch Uploader Plugin for userbot.
{i}upb

"""


@ItzSjDude(outgoing=True, pattern=r"upb")
async def _(event):
    await batch_upload(event)
