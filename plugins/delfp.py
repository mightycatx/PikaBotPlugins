"""Plugin For Removing  n no. Of profile pics
{i}delpfp <no. of pics> """

from . import remppic


@ItzSjDude(outgoing=True, pattern="delpfp ?(.*)")
async def _(delpfp):
    await remppic(delpfp)
