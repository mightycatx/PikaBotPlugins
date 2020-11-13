"""Currency Converter Plugin
{i}currency <from to>"""
#Credits @UniBorg
from . import _currency
@ItzSjDude(outgoing=True, pattern="currency (.*)")
async def _(event):
     await _currency(event)

