"""Profile Related Commands
{i}autobio
**Usage**: Activates Autobio\n
{i}autoname
**Usage**: Activates Autoname\n
{i}autopfp
**Usage**: Activates Autopic\n
{i}avengerspfp
**Usage**: Activates auto Avengers pics\n
{i}animepfp
**Usage**: Activates Anime pics\n
{i}gamerpfp
**Usage**: Activates Gamer pics\n
{i}pbio <Bio>
**Usage**: sets Bio\n
{i}pname <Name>
**Usage**: sets Name\n
{i}ppic <Reply to pic>
**Usage**: sets Profile pic\n
"""
from . import anpfp, atb, atnm, avpfp, gmpfp, pbio, pname

@bot.on(pika_sudo(from_client=1, pattern="pbio (.*)"))
@ItzSjDude(outgoing=True, pattern="pbio (.*)")
async def _(event):
    await pbio(event)

if bot2: 
   @bot2.on(pika_sudo(from_client=2, pattern=pbio (.*)"))
   async def _(event):
       await pbio(event)

if bot3: 
   @bot3.on(pika_sudo(from_client=3, pattern=pbio (.*)"))
   async def _(event):
       await pbio(event)

if bot4: 
   @bot4.on(pika_sudo(from_client=4, pattern=pbio (.*)"))
   async def _(event):
       await pbio(event)

@bot.on(pika_sudo(from_client=1, pattern=pname ((.|\n)*)"))
@ItzSjDude(outgoing=True, pattern="pname ((.|\n)*)")
async def _(event):
    await pname(event)

if bot2: 
   @bot2.on(pika_sudo(from_client=2, pattern=pname ((.|\n)*)"))
   async def _(event):
       await pname(event)

if bot3: 
   @bot3.on(pika_sudo(from_client=3, pattern=pname ((.|\n)*)"))
   async def _(event):
       await pname(event)

if bot4: 
   @bot4.on(pika_sudo(from_client=4, pattern=pname ((.|\n)*)"))
   async def _(event):
       await pname(event)

@bot.on(pika_sudo(from_client=1, pattern="animepfp ?(.*)"))
@ItzSjDude(outgoing=True, pattern="animepfp ?(.*)")
async def _(event):
    await anpfp(event)
if bot2: 
   @bot.on(pika_sudo(from_client=2, pattern="animepfp ?(.*)"))
   async def _(event):
       await anpfp(event)

if bot3: 
   @bot3.on(pika_sudo(from_client=3, pattern="animepfp ?(.*)"))
   async def _(event):
       await anpfp(event)

if bot3: 
   @bot4.on(pika_sudo(from_client=4, pattern="animepfp ?(.*)"))
   async def _(event):
       await anpfp(event)

@bot.on(pika_sudo(from_client=1, pattern="avengerspfp ?(.*)"))
@ItzSjDude(outgoing=True, pattern="avengerspfp ?(.*)")
async def _(event):
    await avpfp(event)

if bot2:
   @bot2.on(pika_sudo(from_client=2, pattern="avengerspfp ?(.*)"))
   async def _(event):
       await avpfp(event)

if bot3:
   @bot3.on(pika_sudo(from_client=3, pattern="avengerspfp ?(.*)"))
   async def _(event):
       await avpfp(event)

if bot4:
   @bot4.on(pika_sudo(from_client=4, pattern="avengerspfp ?(.*)"))
   async def _(event):
       await avpfp(event)

@bot.on(pika_sudo(from_client=1, pattern="gamerpfp ?(.*)"))
@ItzSjDude(outgoing=True, pattern="gamerpfp ?(.*)")
async def _(event):
    await gmpfp(event)

if bot2: 
   @bot2.on(pika_sudo(from_client=2, pattern="gamerpfp ?(.*)"))
   async def _(event):
       await gmpfp(event)

if bot3: 
   @bot3.on(pika_sudo(from_client=3, pattern="gamerpfp ?(.*)"))
   async def _(event):
       await gmpfp(event)

if bot4: 
   @bot4.on(pika_sudo(from_client=4, pattern="gamerpfp ?(.*)"))
   async def _(event):
       await gmpfp(event)

@bot.on(pika_sudo(from_client=1, pattern="autoname$"))
@ItzSjDude(outgoing=True, pattern="autoname$")
async def _(event):
    await atnm(event)

if bot2:
   @bot2.on(pika_sudo(from_client=2, pattern="autoname$"))
   async def _(event):
       await atnm(event)

if bot3:
   @bot3.on(pika_sudo(from_client=3, pattern="autoname$"))
   async def _(event):
       await atnm(event)

if bot4:
   @bot4.on(pika_sudo(from_client=4, pattern="autoname$"))
   async def _(event):
       await atnm(event)

@bot.on(pika_sudo(from_client=1, pattern="autobio$"))
@ItzSjDude(outgoing=True, pattern="autobio$")
async def _(event):
    await atb(event)

if bot2:
   @bot2.on(pika_sudo(from_client=2, pattern="autobio$"))
   async def _(event):
       await atb(event)

if bot3:
   @bot3.on(pika_sudo(from_client=3, pattern="autobio$"))
   async def _(event):
       await atb(event)

if bot4:
   @bot4.on(pika_sudo(from_client=4, pattern="autobio$"))
   async def _(event):
       await atb(event)
