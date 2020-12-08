#!/usr/bin/env python3
#
# Copyright (C) 2020 by ItzSjDude@Github, < https://github.com/ItzSjDude/PikachuUserbot >.
#
# This file is part of < https://github.com/ItzSjDude/PikachuUserbot > project,
# and is released under the "GNU v3.0 License Agreement".
#
# Please see < https://github.com/ItzSjDude/PikachuUserbot/blob/master/LICENSE >
#
# All rights reserved

"""**PikaBot db Reset Module**\n
{i}resetdb
**Usage**: Resets pmpermit, filter, notes, snips and Other Db Plugins """
from pikabot.Event_Handlers.pika_db import pika_db_reset


@ItzSjDude(pattern="dbrset$", outgoing=True)
async def reset_db(db):
    try:
        pika_db_reset()
        await db.edit("**Resetting Db...**\n Eta: 30secs")
        await asyncio.sleep(20)
    except Exception as e:
        await db.edit(f"**Error**: {e}")
    await db.edit("**Sucessfully reseted PikaBot DB**\n Restarting Now... \n Eta: 1min")
    pikarestart()


# ©t.me/ItzSjDude
