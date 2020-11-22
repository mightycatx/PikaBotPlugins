# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
"""Spamming Modules
\n{i}tspam <text>
Usage: Spam the text letter by letter.
\n{i}spam <count> <text>
Usage: Your regular spammer stuff :P\
\n{i}bigspam <count> <text>\
Usage: .spam on steroids !!\
\n{i}picspam <count> <link>\
Usage: As if text spam was not enough !!
\n{i}dspam <delay> <count> <text>
Usage: bigspam but slower.
\n{i}gangsta
Usage: Gives you Gendgster Feeling
\n{i}nikal\
\nUsage: Randi Rona
\nNOTE : I am not responsible if you get banned for spamming!"""

import asyncio

BOTLOG = Var.BOTLOG_CHATID


@ItzSjDude(outgoing=True, pattern="spam (.*)")
async def spammer(e):
    counter = int(e.pattern_match.group(1).split(" ", 1)[0])
    spam_message = str(e.pattern_match.group(1).split(" ", 1)[1])
    await e.delete()
    await asyncio.wait([e.respond(spam_message) for i in range(counter)])
    if BOTLOG:
        await e.client.send_message(
            BOTLOG_CHATID, "#SPAM\n" "Spam was executed successfully"
        )


@ItzSjDude(outgoing=True, pattern="bigspam (.*)")
async def bigspam(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@"):
        message = e.text
        counter = int(message[9:13])
        spam_message = str(e.text[13:])
        for i in range(1, counter):
            await e.respond(spam_message)
        await e.delete()
        if BOTLOG:
            await e.client.send_message(
                BOTLOG, "#BIGSPAM \n\n" "Bigspam was executed successfully"
            )


@ItzSjDude(outgoing=True, pattern="gangsta$")
async def whoizme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@"):
        await e.edit("EVERyBOdy")
        await asyncio.sleep(0.3)
        await e.edit("iZ")
        await asyncio.sleep(0.2)
        await e.edit("GangSTur")
        await asyncio.sleep(0.5)
        await e.edit("UNtIL ")
        await asyncio.sleep(0.2)
        await e.edit("I")
        await asyncio.sleep(0.3)
        await e.edit("ArRivE")
        await asyncio.sleep(0.3)
        await e.edit("🔥")
        await asyncio.sleep(0.3)
        await e.edit("EVERyBOdy iZ GangSTur UNtIL I ArRivE 🔥")


@ItzSjDude(outgoing=True, pattern="nikal$")
async def whoizme(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@"):
        await e.edit("NikAl")
        await asyncio.sleep(0.3)
        await e.edit("lAwDe")
        await asyncio.sleep(0.2)
        await e.edit("PehLi")
        await asyncio.sleep(0.5)
        await e.edit("FuRsaT")
        await asyncio.sleep(0.2)
        await e.edit("Me")
        await asyncio.sleep(0.3)
        await e.edit("NikAl")
        await asyncio.sleep(0.3)
        await e.edit("<--")
        await asyncio.sleep(0.3)
        await e.edit("NikAl lAwDe PehLi FuRsaT Me NikAL <--")


@ItzSjDude(outgoing=True, pattern="rspam (.*)")
async def repeats(e):
    message = e.text[8:]
    count = int(e.text[6:8])
    repmessage = message * count
    await wait([e.respond(repmessage) for i in range(count)])
    await e.delete()


@ItzSjDude(outgoing=True, pattern="picspam (.*)")
async def tiny_pic_spam(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@"):
        message = e.text
        text = message.split()
        counter = int(text[0])
        link = str(text[2])
        if range(1, counter):
            await e.client.send_file(e.chat_id, link)
        await e.delete()
        if BOTLOG:
            await e.client.send_message(
                BOTLOG, "#PICSPAM \n\n" "PicSpam was executed successfully"
            )


@ItzSjDude(outgoing=True, pattern="delayspam (.*)")
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@"):
        message = e.text
        spamDelay = float(message[11:15])
        counter = int(message[15:19])
        spam_message = str(e.text[19:])
        for i in range(1, counter):
            await e.respond(spam_message)
            time.sleep(spamDelay)
        await e.delete()
        if BOTLOG:
            await e.client.send_message(
                BOTLOG, "#DelaySPAM \n\n" "DelaySpam was executed successfully"
            )
