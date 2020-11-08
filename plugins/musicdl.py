""" Spotify / Deezer downloader plugin by @anubisxx | Syntax: .sdd link"""
import asyncio

from pikabot.utils import ItzSjDude
from telethon.errors.rpcerrorlist import (
    UserAlreadyParticipantError,
    YouBlockedUserError,
)
from telethon.tl.functions.messages import ImportChatInviteRequest


@ItzSjDude(outgoing=True, pattern="sdd ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    d_link = event.pattern_match.group(1)
    if ".com" not in d_link:
        await event.edit("` I need a link to download something pro.`**(._.)**")
    else:
        await event.edit("🎶**Initiating Download!**🎶")

    async with event.client.conversation("@DeezLoadBot") as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            try:
                await event.client(ImportChatInviteRequest("AAAAAFZPuYvdW1A8mrT8Pg"))
            except UserAlreadyParticipantError:
                await asyncio.sleep(0.00000069420)
            await conv.send_message(d_link)
            details = await conv.get_response()
            await event.client.send_message(event.chat_id, details)
            await conv.get_response()
            songh = await conv.get_response()
            await event.client.send_file(
                event.chat_id,
                songh,
                caption="🔆**Here's the requested song!**🔆\n`Check out` [Pikachu Userbot](t.me/PikachuUserbot)",
            )
            await event.delete()
        except YouBlockedUserError:
            await event.edit("**Error:** `unblock` @DeezLoadBot `and retry!`")
