from . import helper, pika_sudo

@bot.on(pika_sudo(from_client=1, pattern=r"help ?(.*)"))
@ItzSjDude(outgoing=True, pattern=r"help ?(.*)")
async def _(event):
    await helper(event)
