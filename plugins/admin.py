# Officially made for Pikabot by ItzSjDude from Paperplane extended snippets

from . import (
    _ban,
    _demote,
    _gadmin,
    _gmte,
    _gusers,
    _kick,
    _mute,
    _pin,
    _promote,
    _rmdacc,
    _setgpic,
    _unban,
    _ungmute,
    _unmute,
)


@ItzSjDude(groups_only=True, pattern=r"setgpic$")
async def _(gpic):
    await _setgpic(gpic)


@ItzSjDude(groups_only=True, pattern=r"promote(?: |$)(.*)")
async def _(promt):
    await _promote(promt)


@ItzSjDude(groups_only=True, pattern=r"demote(?: |$)(.*)")
async def _(dmod):
    await _demote(dmod)


@ItzSjDude(groups_only=True, pattern=r"ban(?: |$)(.*)")
async def _(bon):
    await _ban(bon)


@ItzSjDude(groups_only=True, pattern=r"unban(?: |$)(.*)")
async def _(unbon):
    await _unban(unbon)


@ItzSjDude(groups_only=True, pattern=r"mute(?: |$)(.*)")
async def _(spdr):
    await _mute(spdr)


@ItzSjDude(groups_only=True, pattern=r"unmute(?: |$)(.*)")
async def _(unmot):
    await _unmute(unmot)


@ItzSjDude(groups_only=True, pattern=r"ungmute(?: |$)(.*)")
async def _(un_gmute):
    await _ungmute(un_gmute)


@ItzSjDude(groups_only=True, pattern=r"gmute(?: |$)(.*)")
async def _(gspdr):
    await _gmte(gspdr)


@ItzSjDude(groups_only=True, pattern=r"delusers(?: |$)(.*)")
async def _(show):
    await _rmdacc(show)


@ItzSjDude(groups_only=True, pattern=r"adminlist$")
async def _(show):
    await _gadmin(show)


@ItzSjDude(groups_only=True, pattern=r"pin(?: |$)(.*)")
async def _(msg):
    await _pin(msg)


@ItzSjDude(groups_only=True, pattern=r"kick(?: |$)(.*)")
async def _(usr):
    await _kick(usr)


@ItzSjDude(groups_only=True, pattern=r"users ?(.*)")
async def _(show):
    await _gusers(show)
