"""
{i}setwelcome <welcome message> or reply to msg
**Usage**: Sets the message as a welcome note in the chat
{i}getwelcome
**Usage**: Shows current welcome note in the chat\n
{i}delwelcome
**Usage**: Deletes the welcome note from current chat\n\n
**Available formats for formatting welcome Note**:
`{mention}, {title}, {count}, {first}, {last}, {fullname}, {userid}, {username}, {my_first}, {my_fullname}, {my_last}, {my_mention}, {my_username}`
"""

from . import ChatAction, _welcome, del_welcm, get_welcm, set_wlcm


@bot.on(ChatAction)
async def _(_pika):
    await _welcome(_pika)


@ItzSjDude(outgoing=True, pattern=r"setwelcome(?: |$)(.*)")
async def _(_pika):
    await set_wlcm(_pika)


@ItzSjDude(outgoing=True, pattern="getwelcome$")
async def _(_pika):
    await get_welcm(_pika)


@ItzSjDude(outgoing=True, pattern="delwelcome$")
async def _(_pika):
    await del_welcm(_pika)
