"""Spamming Module
{i}spam <no of msgs> <msg>

Note:- Don't use to much"""

# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

from asyncio import wait


@ItzSjDude(outgoing=True, pattern=r"spam")
async def spammer(e):
    message = e.text
    counter = int(message[6:8])
    spam_message = str(e.text[8:])

    await wait([e.respond(spam_message) for i in range(counter)])

    await e.delete()
    if Var.BOTLOG_CHATID:
        await e.client.send_message(
            Var.BOTLOG_CHATID, "#SPAM \n\n" "Spam was executed successfully"
        )
