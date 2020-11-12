"""Alive Plugin for Pikabot
{i}alive
"""
# Made by @ItzSjDude. All Rights Reserved

from . import _alive


@ItzSjDude(outgoing=True, pattern=r"alive$")
async def _(event):
    await _alive(event)
