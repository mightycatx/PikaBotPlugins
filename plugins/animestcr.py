"""Plugin which transforms your text into anime stickers
{i}waifu <yourText>
"""
from . import waifu


@ItzSjDude(pattern="waifu(?: |$)(.*)")
async def _(animu):
    await waifu(animu)
