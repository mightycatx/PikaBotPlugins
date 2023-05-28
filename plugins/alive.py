"""Alive Plugin for Pikabot
{i}alive
"""
# Made by @ItzSjDude. All Rights Reserved

from . import _alive, bot2, bot3, bot4


@ItzSjDude(outgoing=True, pattern=r"alive$")
async def _(event):
    await _alive(event)
