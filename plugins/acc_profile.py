"""Profile Related Commands
{i}autobio
{i}autoname
{i}autopfp
{i}avengerspfp
{i}animepfp
{i}gamerpfp
{i}pbio <Bio>
{i}pname <Name>
{i}ppic <Reply to pic>
"""
from . import pbio,pname,anpfp,avpfp,gmpfp,atnm,atb

@ItzSjDude(outgoing=True, pattern="pbio (.*)")
async def _(event):
    await pbio(event)


@ItzSjDude(outgoing=True, pattern="pname ((.|\n)*)")
async def _(event):
    await pname(event)


@ItzSjDude(outgoing=True, pattern="animepfp ?(.*)")
async def _(event):
    await anpfp(event)


@ItzSjDude(outgoing=True, pattern="avengerspfp ?(.*)")
async def _(event):
    await avpfp(event)


@ItzSjDude(outgoing=True, pattern="gamerpfp ?(.*)")
async def _(event):
    await gmpfp(event)


@ItzSjDude(outgoing=True, pattern="autoname")
async def _(event):
    await atnm(event)


@ItzSjDude(outgoing=True, pattern="autobio")
async def _(event):
    await atb(event)
