"""Ping Module for Pikabot
{i}pika"""

# Made by @ItzSjDude for Pikabot
from . import _ping

@ItzSjDude(outgoing=True, pattern="pika$")
async def _(event):
    await _ping(event)
