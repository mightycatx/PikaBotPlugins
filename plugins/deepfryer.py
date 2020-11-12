#ported by @NeoMatrix90, from paperplane 

"""module for frying stuff
{i}deepfry <reply to image>
"""

@ItzSjDude(outgoing=True, pattern="deepfry(?: |$)(.*)")
async def _(event):
  await deepfryer(event)

