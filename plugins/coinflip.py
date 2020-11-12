"""CoinFlip for PikaBot
{i}coinflip [optional_choice]"""
# credits @Uniborg


@ItzSjDude(outgoing=True, pattern="coin ?(.*)")
async def _(event):
    await cflip(event)
