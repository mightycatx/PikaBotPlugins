import asyncio
import time
from collections import deque

from pikabot.utils import ItzSjDude
from SysRuntime import *
from telethon.tl.functions.channels import LeaveChannelRequest
from userbot import Pika_Cmd, bot


@ItzSjDude(outgoing=True, pattern="leave$")
async def leave(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("`I iz Leaving dis Lol Group kek!`")
        time.sleep(3)
        if "-" in str(e.chat_id):
            await bot(LeaveChannelRequest(e.chat_id))
        else:
            await e.edit("`But Boss! This is Not A Chat`")


@ItzSjDude(outgoing=True, pattern=";_;$")
async def fun(e):
    t = ";__;"
    for j in range(10):
        t = t[:-1] + "_;"
        await e.edit(t)


@ItzSjDude(outgoing=True, pattern="yo$")
async def Ooo(e):
    t = "yo"
    for j in range(15):
        t = t[:-1] + "oo"
        await e.edit(t)


@ItzSjDude(outgoing=True, pattern="Oof$")
async def Oof(e):
    t = "Oof"
    for j in range(15):
        t = t[:-1] + "of"
        await e.edit(t)


@ItzSjDude(outgoing=True, pattern="ccry$")
async def cry(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("(;´༎ຶД༎ຶ)")


@ItzSjDude(outgoing=True, pattern="fp$")
async def facepalm(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("🤦‍♂")


@ItzSjDude(outgoing=True, pattern="moon$")
async def _(event):
    if event.fwd_from:
        return
    deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
    for _ in range(32):
        await asyncio.sleep(0.1)
        await event.edit("".join(deq))
        deq.rotate(1)


@ItzSjDude(outgoing=True, pattern="source$")
async def source(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(f"{sys4}")


@ItzSjDude(outgoing=True, pattern="readme$")
async def reedme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(f"{sys4}/blob/master/README.md")


@ItzSjDude(outgoing=True, pattern="heart$")
async def _(event):
    if event.fwd_from:
        return
    deq = deque(list("❤️🧡💛💚💙💜🖤"))
    for _ in range(32):
        await asyncio.sleep(0.1)
        await event.edit("".join(deq))
        deq.rotate(1)


@ItzSjDude(outgoing=True, pattern="fap$")
async def _(event):
    if event.fwd_from:
        return
    deq = deque(list("🍆✊🏻💦"))
    for _ in range(32):
        await asyncio.sleep(0.1)
        await event.edit("".join(deq))
        deq.rotate(1)


Pika_Cmd.update({"leave": "Leave a Chat"})
Pika_Cmd.update({";__;": "You try it!"})
Pika_Cmd.update({"cry": "Cry"})
Pika_Cmd.update({"fp": "Send face palm emoji."})
Pika_Cmd.update({"moon": "Bot will send a cool moon animation."})
Pika_Cmd.update({"clock": "Bot will send a cool clock animation."})
Pika_Cmd.update({"readme": "Reedme."})
Pika_Cmd.update({"source": "Gives the source of your userbot"})
Pika_Cmd.update({"myusernames": "List of Usernames owned by you."})
Pika_Cmd.update({"oof": "Same as ;__; but ooof"})
Pika_Cmd.update({"earth": "Sends Kensar Earth animation"})
Pika_Cmd.update({"heart": "Try and you'll get your emotions back"})
Pika_Cmd.update({"fap": "Faking orgasm"})
