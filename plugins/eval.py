"""Evaluate Python Code inside Telegram
{i}eval PythonCode"""


@ItzSjDude(outgoing=True, pattern="eval")
async def _(event):
    await eval(event)
