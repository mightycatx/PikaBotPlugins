# © Itzsjdude


from . import ChatAction, _welcome, del_welcm, get_welcm, set_wlcm


@bot.on(ChatAction)
async def _(_pika):
    await _welcome(_pika)


@ItzSjDude(outgoing=True, pattern=r"setwelcome(?: |$)(.*)")
async def _(_pika):
    await set_wlcm(_pika)


@ItzSjDude(outgoing=True, pattern="getwelcome$")
async def _(_pika):
    await get_welcm(_pika)


@ItzSjDude(outgoing=True, pattern="delwelcome$")
async def _(_pika):
    await del_welcm(_pika)
