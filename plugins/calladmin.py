"""Admins notifier plugin
{i}admins"""

from . import spm_notify

@ItzSjDude(outgoing=True, pattern="admins")
async def _(event):
    await spm_notify(event)
