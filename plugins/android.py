""" Userbot module containing commands related to android
{i}magisk
\nGet latest Magisk releases\
{i}device <codename>
Usage: Get info about android device codename or model.
{i}codename <brand> <device>
Usage: Search for android device codename.
\n\n{i}specs <brand> <device>
\nUsage: Get device specifications info.
{i}twrp <codename>
\nUsage: Get latest twrp download for android device."
"""


@ItzSjDude(outgoing=True, pattern="magisk$")
async def _(request):
    await magisk(request)


@ItzSjDude(outgoing=True, pattern=r"device(?: |$)(\S*)")
async def _(request):
    await device_info(request)


@ItzSjDude(outgoing=True, pattern=r"codename(?: |)([\S]*)(?: |)([\s\S]*)")
async def _(request):
    await codename_info(request)


@ItzSjDude(outgoing=True, pattern=r"specs(?: |)([\S]*)(?: |)([\s\S]*)")
async def _(request):
    await dspecs(request)


@ItzSjDude(outgoing=True, pattern=r"twrp(?: |$)(\S*)")
async def _(request):
    await twrp(request)
