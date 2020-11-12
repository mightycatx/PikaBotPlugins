"""Quickly make a decision
{i}decide"""

@ItzSjDude(outgoing=True, pattern="decide")
async def _(event):
  await decide(event)

