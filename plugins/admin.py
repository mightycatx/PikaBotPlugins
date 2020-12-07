# Officially made for Pikabot by ItzSjDude from Paperplane extended snippets
"""**Administration Commands**\n\n
{i}setgpic <reply to image>
**Usage**: Set replied Image as Group Profile pic\n
{i}promote reply to UserMsg or @username <CustomAdmintag>
**Usage**: Promote user with custom admin tag if given\n
{i}demote <reply to UserMsg> or @username
**Usage**: Demotes user from admin\n
{i}ban <reply to UserMsg> or @username
**Usage**: Ban user\n
{i}unban <reply to UserMsg> or @username
**Usage**: Unban user\n
{i}mute <reply to UserMsg> or @username
**Usage**: Mutes user from chat\n
{i}mute <reply to UserMsg> or @username
**Usage**: Unmutes User from Chat\n
{i}gmute <reply to UserMsg> <reason> or @username <reason>
**Usage**: Globally Mutes user nd Add to gban watcher\n
{i}ungmute <reply to UserMsg> or @username
**Usage**: Globally Unmutes Mutes user nd Remove from gmute watcher\n
{i}delusers
**Usage**: Removes Deleted/inactive Users from groups/channels\n
{i}adminlist
**Usage**: get admins in group\n
{i}users
**Usage**: Get all users From group\n
{i}kick reply to UserMsg or @username
**Usage**: kick User from group\n
{i}pin <reply to msg>
**Usage**: Pins replied msg\n
{i}invite <Username>
**Usage**: Invites User to Current Chat
"""

from pikabot.utils import admin_cmd

from . import (
    _ban,
    _demote,
    _gadmin,
    _gmte,
    _gusers,
    _invite,
    _kick,
    _mute,
    _muter,
    _pin,
    _promote,
    _rmdacc,
    _setgpic,
    _unban,
    _ungmute,
    _unmute,
)

try:
    from pikabot import bot, bot2
except BaseException:
    pass


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


@ItzSjDude(groups_only=True, pattern="invite ?(.*)")
async def _(event):
    await _invite(event)


@ItzSjDude(groups_only=True, pattern=r"users ?(.*)")
async def _(show):
    await _gusers(show)


@bot.on(admin_cmd(incoming=True))
async def _(moot):
    await _muter(moot)


if bot2:

    @bot2.on(admin_cmd(incoming=True))
    async def _(moot):
        await _muter(moot)


if bot3:

    @bot3.on(admin_cmd(incoming=True))
    async def _(moot):
        await _muter(moot)


if bot4:

    @bot4.on(admin_cmd(incoming=True))
    async def _(moot):
        await _muter(moot)
