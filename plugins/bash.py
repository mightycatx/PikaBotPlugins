"""For executing linux/Gnu Commands
{i}bash <cmd> """

from . import _bash, pika_sudo, bot, bot2, bot3, bot4

if bot:
  @bot.on(pika_sudo(from_client=1, pattern="bash ?(.*)"))
  async def _(event):
      await _bash(event)

if bot2:
  @bot2.on(pika_sudo(from_client=2, pattern="bash ?(.*)"))
  async def _(event):
      await _bash(event)

if bot3:
  @bot3.on(pika_sudo(from_client=3, pattern="bash ?(.*)"))
  async def _(event):
      await _bash(event)

if bot4:
  @bot4.on(pika_sudo(from_client=4, pattern="bash ?(.*)"))
  async def _(event):
      await _bash(event)

@ItzSjDude(pattern="bash ?(.*)")
async def _(event):
    await _bash(event)
