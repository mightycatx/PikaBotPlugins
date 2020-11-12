"""Alive Plugin for Pikabot
{i}alive
"""
# Made by @ItzSjDude. All Rights Reserved


@ItzSjDude(outgoing=True, pattern=r"alive$")
async def _(event):
    await alive(event)
