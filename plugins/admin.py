# Officially made for Pikabot by ItzSjDude from Paperplane extended snippets


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
    await mute(spdr)


@ItzSjDude(pattern=r"unmute(?: |$)(.*)")
async def _(unmot):
    await unmute(unmot)


@ItzSjDude(pattern=r"ungmute(?: |$)(.*)")
async def _(un_gmute):
    await ungmute(un_gmute)


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


CMD_HELP.update(
    {
        "admin": ".promote <username/reply> <custom rank (optional)>\
\nUsage: Provides admin rights to the person in the chat.\
\n\n.demote <username/reply>\
\nUsage: Revokes the person's admin permissions in the chat.\
\n\n.ban <username/reply> <reason (optional)>\
\nUsage: Bans the person off your chat.\
\n\n.unban <username/reply>\
\nUsage: Removes the ban from the person in the chat.\
\n\n.mute <username/reply> <reason (optional)>\
\nUsage: Mutes the person in the chat, works on admins too.\
\n\n.unmute <username/reply>\
\nUsage: Removes the person from the muted list.\
\n\n.gmute <username/reply> <reason (optional)>\
\nUsage: Mutes the person in all groups you have in common with them.\
\n\n.ungmute <username/reply>\
\nUsage: Reply someone's message with .ungmute to remove them from the gmuted list.\
\n\n.delusers\
\nUsage: Searches for deleted accounts in a group. Use .delusers clean to remove deleted accounts from the group.\
\n\n.admins\
\nUsage: Retrieves a list of admins in the chat.\
\n\n.users or .users <name of member>\
\nUsage: Retrieves all (or queried) users in the chat.\
\n\n.setgppic <reply to image>\
\nUsage: Changes the group's display picture."
    }
)
