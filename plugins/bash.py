"""For executing linux/Gnu Commands
{i}bash <cmd> """

@ItzSjDude(pattern="bash ?(.*)")
async def _(event):
  await bash(event)
