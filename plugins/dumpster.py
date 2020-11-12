"""Dumping Animation Plugin
{i}dump"""

@ItzSjDude(outgoing=True, pattern="dump ?(.*)")
async def _(message):
    await dump(message):
