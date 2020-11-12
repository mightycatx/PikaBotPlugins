# Copyright (C) 2019 The Raphielscape Company LLC.


"""Direct links generator
{i}direct <url> <url>

__Supported Websites__
MEGA.nz 
MediaFire
Google Drive 
Cloud Mail 
Yandex.Disk 
AFH-ZippyShare
SourceForge 
OSDN-GitHub
"""

@ItzSjDude(outgoing=True, pattern=r"direct(?: |$)([\s\S]*)")
async def _(request):
    await dlg(request)

