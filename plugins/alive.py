"""Alive Plugin for Pikabot
{i}alive
"""
# Made by @ItzSjDude. All Rights Reserved

from . import _alive, bot2, bot3, bot4, pika_sudo

if bot2:
    @bot2.on(pika_sudo(from_client=2, pattern=r"alive$"))
    async def _(event):
        await _alive(event)

if bot3:
    @bot3.on(pika_sudo(from_client=3, pattern=r"alive$"))
    async def _(event):
        await _alive(event)

if bot4:
    @bot4.on(pika_sudo(from_client=4, pattern=r"alive$"))
    async def _(event):
        await _alive(event)

@ItzSjDude(outgoing=True, pattern=r"alive$")
@bot.on(pika_sudo(from_client=1, pattern=r"alive$"))
async def _(event):
    await _alive(event)
