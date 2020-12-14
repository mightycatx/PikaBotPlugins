"""Check your internet speed powered by speedtest.net
{i}speedtest <image/file/text> 
"""
from datetime import datetime

import speedtest
from . import _speedtest

@ItzSjDude(outgoing=True, pattern="speedtest ?(.*)")
async def _(event):
    await _speedtest(event)

