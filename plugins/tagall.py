# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


""Tag all
{i}tagall"""

from uniborg.util import admin_cmd
@ItzSjDude(pattern="tagall")
async def _(event):
    if event.fwd_from:
        return
    mentions = "Attention Please"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, 100):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    await event.reply(mentions)
    await event.delete()
