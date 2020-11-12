"""
Telegram Channel Media Downloader Plugin for userbot.
usage: {i}geta channel_username [will  get all media from channel, tho there is limit of 3000 there to prevent API limits.]
       {i}getc number_of_messsages channel_username
"""
# By: @Zero_cool7870


@ItzSjDude(outgoing=True, pattern=r"getc")
async def _(event):
    await get_media(event)


@ItzSjDude(pattern=r"geta")
async def _(event):
    await getmedia(event)
