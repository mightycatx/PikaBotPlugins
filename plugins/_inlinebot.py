"""©ItzSjDude Officially made for PikachuUserbot"""

import asyncio
import math
import os
import re

from pikabot import ALIVE_NAME, CMD_LIST
from telethon import custom, events
from var import Var

try:
    from pikabot import bot2, bot3, bot4
except BaseException:
    pass

b1 = bot.me
if bot2:
    b2 = bot2.me
else:
    b2 = b1
if bot3:
    b3 = bot3.me
else:
    b3 = b1
if bot4:
    b4 = bot4.me
else:
    b4 = b1

emoji = os.environ.get("INLINE_EMOJI", "")
incols = int(os.environ.get("INLINE_COLUMNS", 3))
inrows = int(os.environ.get("INLINE_ROWS", 7))
if emoji is not None:
    xl = emoji
else:
    xl = ""
if incols is not None:
    pikcl = incols
else:
    pikcl = 3

if inrows is not None:
    pikrws = inrows
else:
    pikrws = 7
if Var.TG_BOT_USER_NAME_BF_HER is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)  # pylint:disable=E0602
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if (
            event.query.user_id == b1.id
            or event.query.user_id == b2.id
            or event.query.user_id == b3.id
            or event.query.user_id == b4.id
            and query.startswith("Pïkå¢hµ")
        ):
            rev_text = query[::-1]
            buttons = paginate_help(0, CMD_LIST, "helpme")
            result = builder.article(
                "©Pikachu Userbot Help",
                text="{}\nCurrently Loaded Plugins: {}".format(query, len(CMD_LIST)),
                buttons=buttons,
                link_preview=False,
            )
        await event.answer([result] if result else None)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(rb"helpme_next\((.+?)\)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if (
            event.query.user_id == b1.id
            or event.query.user_id == b2.id
            or event.query.user_id == b3.id
            or event.query.user_id == b4.id
            and query.startswith("Pïkå¢hµ")
        ):
            current_page_number = int(event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(current_page_number + 1, CMD_LIST, "helpme")
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)

        else:
            reply_pop_up_alert = "Please get your own PikaBot, and don't use mine!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(rb"helpme_prev\((.+?)\)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if (
            event.query.user_id == b1.id
            or event.query.user_id == b2.id
            or event.query.user_id == b3.id
            or event.query.user_id == b4.id
            and query.startswith("Pïkå¢hµ")
        ):
            current_page_number = int(event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(
                current_page_number - 1, CMD_LIST, "helpme"  # pylint:disable=E0602
            )
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)

        else:
            reply_pop_up_alert = "Please get your own PikaBot, and don't use mine!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"restart")))
    async def on_plug_in_callback_query_handler(event):
        usr = event.query
        if (
            usr.user_id == b1.id
            or usr.user_id == b2.id
            or usr.user_id == b3.id
            or usr.user_id == b4.id
        ):
            a = await event.edit("Pika Pi! Restarting wait for 1 Min!")
            pika_start()
            await a.delete()
        else:
            reply_pop_up_alert = "You can't Restart me, Get your own Pikachu Userbot"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        usr = event.query
        if (
            usr.user_id == b1.id
            or usr.user_id == b2.id
            or usr.user_id == b3.id
            or usr.user_id == b4.id
        ):
            await event.edit("Pika Pi! Menu Closed!")

        else:
            reply_pop_up_alert = (
                "You can't close this menu ploxx, Get your own Pikachu Userbot"
            )
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"us_plugin_(.*)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        usr = event.query
        if (
            usr.user_id == b1.id
            or usr.user_id == b2.id
            or usr.user_id == b3.id
            or usr.user_id == b4.id
            and query.startswith("Pïkå¢hµ")
        ):
            plugin_name = event.data_match.group(1).decode("UTF-8")
            help_string = CMD_LIST[plugin_name].__doc__.format(i=rx)

            reply_pop_up_alert = (
                help_string
                if help_string is not None
                else "No DOCSTRING has been setup for {} plugin".format(plugin_name)
            )
            reply_pop_up_alert += "\n\n©PikaBot"
            if len(help_string) >= 140:
                pop_up = "Command list too long check Saved Messages"
                help_string += "\n\n **Self distructing in 15secs**"
                await event.answer(pop_up, cache_time=0, alert=True)
                if bot is not None and event.query.user_id == bot.uid:
                    a = await bot.send_message("me", help_string)
                    await asyncio.sleep(15)
                    await a.delete()
                if bot2 is not None and event.query.user_id == bot2.uid:
                    a = await bot2.send_message("me", help_string)
                    await asyncio.sleep(15)
                    await a.delete()
                if bot3 is not None and event.query.user_id == bot3.uid:
                    a = await bot3.send_message("me", help_string)
                    await asyncio.sleep(15)
                    await a.delete()
                if bot4 is not None and event.query.user_id == bot4.uid:
                    a = await bot4.send_message("me", help_string)
                    await asyncio.sleep(15)
                    await a.delete()

            else:
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        else:
            reply_pop_up_alert = "Hi {}'s bot here ,\n\nWhy r u clicking this this.Please get your own PikaBot, and don't use mine!".format(
                ALIVE_NAME
            )
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


def paginate_help(page_number, loaded_plugins, prefix):

    number_of_rows = pikrws
    number_of_cols = pikcl
    helpable_plugins = []
    pfix = ["_", "herok", "tool"]
    for p in loaded_plugins:
        if not p.startswith(tuple(pfix)):
            helpable_plugins.append(p)

    helpable_plugins = sorted(helpable_plugins)
    modules = [
        custom.Button.inline(
            "{} {} {}".format(xl, x, xl), data="us_plugin_{}".format(x)
        )
        for x in helpable_plugins
    ]

    if number_of_cols == 1:
        pairs = list(zip(modules[::number_of_cols]))
    elif number_of_cols == 2:
        pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    else:
        pairs = list(
            zip(
                modules[::number_of_cols],
                modules[1::number_of_cols],
                modules[2::number_of_cols],
            )
        )
    max_num_pages = math.ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = (
            [
                (
                    custom.Button.inline(
                        "«]", data="{}_prev({})".format(prefix, modulo_page)
                    ),
                    custom.Button.inline("Close🙅‍♀️", data="close"),
                    custom.Button.inline(
                        "[»", data="{}_next({})".format(prefix, modulo_page)
                    ),
                )
            ]
            + pairs[modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)]
            + [(custom.Button.inline("🤖Restart Me", data="restart"),)]
        )

    return pairs
