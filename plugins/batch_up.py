"""
Files Batch Uploader Plugin for userbot.
{i}upb

"""
from . import batch_upload

@ItzSjDude(outgoing=True, pattern=r"upb")
async def _(event):
    await batch_upload(event)
