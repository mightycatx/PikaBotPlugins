"""Bombs Animation Plugin For Pikabot
{i}bombs"""

#EMOJI CONSTANTS
DART_E_MOJI = "🎯"
DICE_E_MOJI = "🎲"
BALL_E_MOJI = "🏀"
# EMOJI CONSTANTS

from pikabot.utils import ItzSjDude
from telethon.tl.types import InputMediaDice


@ItzSjDude(pattern="bombs")
async def _(event):
    await bombs(event)

@ItzSjDude(outgoing=True, pattern=r"call")
async def call(event):
    await call(event)

import asyncio
from collections import deque

from pikabot.utils import ItzSjDude


@ItzSjDude(outgoing=True, pattern="coin ?(.*)")
async def _(event):
    await cflip(event)

from . import _ding


@ItzSjDude(outgoing=True, pattern=r"ding")
async def _(event):
    await _ding(event)

@ItzSjDude(outgoing=True, pattern=r"clock")
async def _(event):
    if event.fwd_from:
        return
    deq = deque(list("🕛🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚"))
    for _ in range(60):
        await asyncio.sleep(0.1)
        await event.edit("".join(deq))
        deq.rotate(1)

@ItzSjDude(outgoing=True, pattern=f"({DART_E_MOJI}|{DICE_E_MOJI}|{BALL_E_MOJI}) ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while not r.media.value == required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except BaseException:
            pass
