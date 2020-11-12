"""Color Plugin for PikaBot
{i}color <color_code>"""
# credits @Uniborg

@ItzSjDude(outgoing=True, pattern="color (.*)")
async def _(event):
  await findcolour(event)

