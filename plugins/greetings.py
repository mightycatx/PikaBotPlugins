"""Greetings plugin
{i}gm
Usage: Good Morning art

{i}gn
Usage: Good Night art

{i}lul
Usage: Lol Art

{i}like
Usage: Like art
"""
from pikabot.sql_helper.global_variables import *


@ItzSjDude(pattern="gn$")
async def gn(event):
    await event.edit(GN)


@ItzSjDude(pattern="gm$")
async def gm(event):
    await event.edit(GM)


@ItzSjDude(pattern="lul$")
async def _(event):
    await event.edit(LOL)


@ItzSjDude(pattern="like$")
async def _(event):
    await event.edit(LIKE)
