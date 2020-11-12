"""Dumping Animation Plugin
{i}dump"""
from . import dump
@ItzSjDude(outgoing=True, pattern="dump ?(.*)")
async def _(message):
    await dump(message)
