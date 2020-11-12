"""Alive Plugin for Pikabot
{i}alive
"""
# Made by @ItzSjDude. All Rights Reserved

from .plugins import alive

@ItzSjDude(outgoing=True, pattern=r"alive$")
async def _(event):
    await alive(event)
