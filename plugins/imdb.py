# For UniBorg
# Copyright (c) JeepBot | 2019
# (c) JeepBot is not occur to all modules in here
"""**Imdb Module**/n
{i}imdb <query>
"""
from . import _imdb

# kanged from Blank-x ;---;


@ItzSjDude(outgoing=True, pattern="imdb (.*)")
async def _(e):
    await _imdb(e)
