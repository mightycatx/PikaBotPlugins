# Officially made for Pikabot by ItzSjDude from Paperplane extended snippets

from . import (
    _mute,
    ban,
    demote,
    get_admin,
    get_users,
    gmte,
    pin,
    promote,
    rm_dacc,
    setgpic,
    unban,
    _ungmute,
    unmute,
)


@ItzSjDude(outgoing=True, pattern=r"setgpic")
async def _(gpic):
    await setgpic(gpic)


@ItzSjDude(outgoing=True, pattern=r"promote(?: |$)(.*)")
async def _(promt):
    await promote(promt)


@ItzSjDude(outgoing=True, pattern=r"demote(?: |$)(.*)")
async def _(dmod):
    await demote(dmod)


@ItzSjDude(pattern=r"ban(?: |$)(.*)")
async def _(bon):
    await ban(bon)


@ItzSjDude(pattern=r"unban(?: |$)(.*)")
async def _(unbon):
    await unban(unbon)


@ItzSjDude(pattern=r"mute(?: |$)(.*)")
async def _(spdr):
    await _mute(spdr)


@ItzSjDude(pattern=r"unmute(?: |$)(.*)")
async def _(unmot):
    await unmute(unmot)


@ItzSjDude(pattern=r"ungmute(?: |$)(.*)")
async def _(un_gmute):
    await _ungmute(un_gmute)


@ItzSjDude(pattern=r"gmute(?: |$)(.*)")
async def _(gspdr):
    await gmte(gspdr)


@ItzSjDude(pattern=r"delusers(?: |$)(.*)")
async def _(show):
    await rm_dacc(show)


@ItzSjDude(pattern=r"adminlist")
async def _(show):
    await get_admin(show)


@ItzSjDude(pattern=r"pin(?: |$)(.*)")
async def _(msg):
    await pin(msg)


@ItzSjDude(pattern=r"kick(?: |$)(.*)")
async def _(usr):
    await kick(usr)


@ItzSjDude(outgoing=True, pattern=r"users ?(.*)")
async def _(show):
    await get_users(show)
