from . import helper, pika_sudo, bot, bot2, bot3, bot4

# ____Sudo____
if bot:

    @bot.on(pika_sudo(from_client=1, pattern=r"help ?(.*)"))
    async def _(event):
        await helper(event)


if bot2:

    @bot2.on(pika_sudo(from_client=2, pattern=r"help ?(.*)"))
    async def _(event):
        await helper(event)


if bot3:

    @bot3.on(pika_sudo(from_client=3, pattern=r"help ?(.*)"))
    async def _(event):
        await helper(event)


if bot4:

    @bot4.on(pika_sudo(from_client=4, pattern=r"help ?(.*)"))
    async def _(event):
        await helper(event)


# ____Main/Multiclients____


@ItzSjDude(outgoing=True, pattern=r"help ?(.*)")
async def _(event):
    await helper(event)
