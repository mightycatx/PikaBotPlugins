"""Admins notifier plugin
{i}admins"""


@ItzSjDude(outgoing=True, pattern="admins")
async def _(event):
    await spm_notify(event)
