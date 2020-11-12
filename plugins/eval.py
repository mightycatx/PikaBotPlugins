"""Evaluate Python Code inside Telegram
{i}eval PythonCode"""

from . import _eval 

@ItzSjDude(outgoing=True, pattern="eval")
async def _(event):
    await _eval(event)
