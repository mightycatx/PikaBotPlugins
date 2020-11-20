import asyncio
import io
import json
import logging
import math
import os
import random
import re
import subprocess
import sys
import time
import traceback
import urllib.parse
from asyncio import sleep
from os import remove
from random import choice, randint, uniform
from subprocess import PIPE, Popen
from time import sleep
from urllib.parse import quote_plus

import pyfiglet
import requests
from bs4 import BeautifulSoup
from humanize import naturalsize
from pikabot import *
from pikabot.handler import *
from pikabot.main_plugs.pfpdata import *
from pikabot.main_plugs.plug import *
from pikabot.main_plugs.SysRuntime import *
from pikabot.utils import *
from pikabot.utils import get_readable_time as grt
from PIL import Image, ImageColor, ImageEnhance, ImageOps
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telethon import custom, events
from telethon.errors import (
    BadRequestError,
    ChatAdminRequiredError,
    FloodWaitError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
    UserAdminInvalidError,
)
from telethon.errors.rpcerrorlist import (
    MessageTooLongError,
    UserIdInvalidError,
    YouBlockedUserError,
)
from telethon.tl import functions
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import SaveDraftRequest, UpdatePinnedMessageRequest
from telethon.tl.functions.photos import DeletePhotosRequest, GetUserPhotosRequest
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
    ChatAdminRights,
    ChatBannedRights,
    DocumentAttributeFilename,
    InputPhoto,
    MessageEntityMentionName,
    MessageMediaPhoto,
)
from telethon.utils import pack_bot_file_id
from var import Var
from var import Var as Config

from ._importer import *

CARBONLANG = "auto"
LANG = "en"

try:
    from pikabot import bot, bot2, bot3, bot4
except BaseException:
    pass
tgbot = bot.tgbot
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
rx = Var.CUSTOM_CMD
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

# ===================== Constants ===========================
PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing the image`"
NO_ADMIN = "`I am not an admin!`"
NO_PERM = "`I don't have sufficient permissions!`"
NO_SQL = "`Running on Non-SQL mode!`"

CHAT_PP_CHANGED = "`Chat Picture Changed`"
CHAT_PP_ERROR = (
    "`Some issue with updating the pic,`"
    "`maybe coz I'm not an admin,`"
    "`or don't have enough rights.`"
)
INVALID_MEDIA = "`Invalid Extension`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================

GITHUB = "https://github.com"
DEVICES_DATA = (
    "https://raw.githubusercontent.com/androidtrackers/"
    "certified-android-devices/master/devices.json"
)
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+"
)

CongoStr = [
    "`Congratulations and BRAVO!`",
    "`You did it! So proud of you!`",
    "`This calls for celebrating! Congratulations!`",
    "`I knew it was only a matter of time. Well done!`",
    "`Congratulations on your well-deserved success.`",
    "`Heartfelt congratulations to you.`",
    "`Warmest congratulations on your achievement.`",
    "`Congratulations and best wishes for your next adventure!”`",
    "`So pleased to see you accomplishing great things.`",
    "`Feeling so much joy for you today. What an impressive achievement!`",
]


DEL_TIME_OUT = 60
DUSER = str(ALIVE_NAME) if ALIVE_NAME else "PikaBot"
DBIO = str(AUTO_BIO) if AUTO_BIO else "Pika is Love 🔥"


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, "", inputString)


def subprocess_run(cmd):
    reply = ""
    subproc = Popen(
        cmd,
        stdout=PIPE,
        stderr=PIPE,
        shell=True,
        universal_newlines=True,
        executable="bash",
    )
    talk = subproc.communicate()
    exitCode = subproc.returncode
    if exitCode != 0:
        reply += (
            "```An error was detected while running the subprocess:\n"
            f"exit code: {exitCode}\n"
            f"stdout: {talk[0]}\n"
            f"stderr: {talk[1]}```"
        )
        return reply
    return talk


def gdrive(url: str) -> str:
    """ GDrive direct links generator """
    drive = "https://drive.google.com"
    try:
        link = re.findall(r"\bhttps?://drive\.google\.com\S+", url)[0]
    except IndexError:
        reply = "`No Google drive links found`\n"
        return reply
    file_id = ""
    reply = ""
    if link.find("view") != -1:
        file_id = link.split("/")[-2]
    elif link.find("open?id=") != -1:
        file_id = link.split("open?id=")[1].strip()
    elif link.find("uc?id=") != -1:
        file_id = link.split("uc?id=")[1].strip()
    url = f"{drive}/uc?export=download&id={file_id}"
    download = requests.get(url, stream=True, allow_redirects=False)
    cookies = download.cookies
    try:
        # In case of small file size, Google downloads directly
        dl_url = download.headers["location"]
        if "accounts.google.com" in dl_url:  # non-public file
            reply += "`Link is not public!`\n"
            return reply
        name = "Direct Download Link"
    except KeyError:
        # In case of download warning page
        page = BeautifulSoup(download.content, "lxml")
        export = drive + page.find("a", {"id": "uc-download-link"}).get("href")
        name = page.find("span", {"class": "uc-name-size"}).text
        response = requests.get(
            export, stream=True, allow_redirects=False, cookies=cookies
        )
        dl_url = response.headers["location"]
        if "accounts.google.com" in dl_url:
            reply += "Link is not public!"
            return reply
    reply += f"[{name}]({dl_url})\n"
    return reply


def zippy_share(url: str) -> str:
    """ZippyShare direct links generator
    Based on https://github.com/LameLemon/ziggy"""
    reply = ""
    dl_url = ""
    try:
        link = re.findall(r"\bhttps?://.*zippyshare\.com\S+", url)[0]
    except IndexError:
        reply = "`No ZippyShare links found`\n"
        return reply
    session = requests.Session()
    base_url = re.search("http.+.com", link).group()
    response = session.get(link)
    page_soup = BeautifulSoup(response.content, "lxml")
    scripts = page_soup.find_all("script", {"type": "text/javascript"})
    for script in scripts:
        if "getElementById('dlbutton')" in script.text:
            url_raw = re.search(
                r"= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);", script.text
            ).group("url")
            math = re.search(
                r"= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);", script.text
            ).group("math")
            dl_url = url_raw.replace(math, '"' + str(eval(math)) + '"')
            break
    dl_url = base_url + eval(dl_url)
    name = urllib.parse.unquote(dl_url.split("/")[-1])
    reply += f"[{name}]({dl_url})\n"
    return reply


def yandex_disk(url: str) -> str:
    """Yandex.Disk direct links generator
    Based on https://github.com/wldhx/yadisk-direct"""
    reply = ""
    try:
        link = re.findall(r"\bhttps?://.*yadi\.sk\S+", url)[0]
    except IndexError:
        reply = "`No Yandex.Disk links found`\n"
        return reply
    api = "https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}"
    try:
        dl_url = requests.get(api.format(link)).json()["href"]
        name = dl_url.split("filename=")[1].split("&disposition")[0]
        reply += f"[{name}]({dl_url})\n"
    except KeyError:
        reply += "`Error: File not found / Download limit reached`\n"
        return reply
    return reply


def cm_ru(url: str) -> str:
    """cloud.mail.ru direct links generator
    Using https://github.com/JrMasterModelBuilder/cmrudl.py"""
    reply = ""
    try:
        link = re.findall(r"\bhttps?://.*cloud\.mail\.ru\S+", url)[0]
    except IndexError:
        reply = "`No cloud.mail.ru links found`\n"
        return reply
    cmd = f"bin/cmrudl -s {link}"
    result = subprocess_run(cmd)
    try:
        result = result[0].splitlines()[-1]
        data = json.loads(result)
    except json.decoder.JSONDecodeError:
        reply += "`Error: Can't extract the link`\n"
        return reply
    except IndexError:
        return reply
    dl_url = data["download"]
    name = data["file_name"]
    size = naturalsize(int(data["file_size"]))
    reply += f"[{name} ({size})]({dl_url})\n"
    return reply


def mediafire(url: str) -> str:
    """ MediaFire direct links generator """
    try:
        link = re.findall(r"\bhttps?://.*mediafire\.com\S+", url)[0]
    except IndexError:
        reply = "`No MediaFire links found`\n"
        return reply
    reply = ""
    page = BeautifulSoup(requests.get(link).content, "lxml")
    info = page.find("a", {"aria-label": "Download file"})
    dl_url = info.get("href")
    size = re.findall(r"\(.*\)", info.text)[0]
    name = page.find("div", {"class": "filename"}).text
    reply += f"[{name} {size}]({dl_url})\n"
    return reply


def sourceforge(url: str) -> str:
    """ SourceForge direct links generator """
    try:
        link = re.findall(r"\bhttps?://.*sourceforge\.net\S+", url)[0]
    except IndexError:
        reply = "`No SourceForge links found`\n"
        return reply
    file_path = re.findall(r"files(.*)/download", link)[0]
    reply = f"Mirrors for __{file_path.split('/')[-1]}__\n"
    project = re.findall(r"projects?/(.*?)/files", link)[0]
    mirrors = (
        f"https://sourceforge.net/settings/mirror_choices?"
        f"projectname={project}&filename={file_path}"
    )
    page = BeautifulSoup(requests.get(mirrors).content, "html.parser")
    info = page.find("ul", {"id": "mirrorList"}).findAll("li")
    for mirror in info[1:]:
        name = re.findall(r"\((.*)\)", mirror.text.strip())[0]
        dl_url = (
            f'https://{mirror["id"]}.dl.sourceforge.net/project/{project}/{file_path}'
        )
        reply += f"[{name}]({dl_url}) "
    return reply


def osdn(url: str) -> str:
    """ OSDN direct links generator """
    osdn_link = "https://osdn.net"
    try:
        link = re.findall(r"\bhttps?://.*osdn\.net\S+", url)[0]
    except IndexError:
        reply = "`No OSDN links found`\n"
        return reply
    page = BeautifulSoup(requests.get(link, allow_redirects=True).content, "lxml")
    info = page.find("a", {"class": "mirror_link"})
    link = urllib.parse.unquote(osdn_link + info["href"])
    reply = f"Mirrors for __{link.split('/')[-1]}__\n"
    mirrors = page.find("form", {"id": "mirror-select-form"}).findAll("tr")
    for data in mirrors[1:]:
        mirror = data.find("input")["value"]
        name = re.findall(r"\((.*)\)", data.findAll("td")[-1].text.strip())[0]
        dl_url = re.sub(r"m=(.*)&f", f"m={mirror}&f", link)
        reply += f"[{name}]({dl_url}) "
    return reply


def androidfilehost(url: str) -> str:
    """ AFH direct links generator """
    try:
        link = re.findall(r"\bhttps?://.*androidfilehost.*fid.*\S+", url)[0]
    except IndexError:
        reply = "`No AFH links found`\n"
        return reply
    fid = re.findall(r"\?fid=(.*)", link)[0]
    session = requests.Session()
    user_agent = useragent()
    headers = {"user-agent": user_agent}
    res = session.get(link, headers=headers, allow_redirects=True)
    headers = {
        "origin": "https://androidfilehost.com",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": user_agent,
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-mod-sbb-ctype": "xhr",
        "accept": "*/*",
        "referer": f"https://androidfilehost.com/?fid={fid}",
        "authority": "androidfilehost.com",
        "x-requested-with": "XMLHttpRequest",
    }
    data = {"submit": "submit", "action": "getdownloadmirrors", "fid": f"{fid}"}
    mirrors = None
    reply = ""
    error = "`Error: Can't find Mirrors for the link`\n"
    try:
        req = session.post(
            "https://androidfilehost.com/libs/otf/mirrors.otf.php",
            headers=headers,
            data=data,
            cookies=res.cookies,
        )
        mirrors = req.json()["MIRRORS"]
    except (json.decoder.JSONDecodeError, TypeError):
        reply += error
    if not mirrors:
        reply += error
        return reply
    for item in mirrors:
        name = item["name"]
        dl_url = item["url"]
        reply += f"[{name}]({dl_url}) "
    return reply


def useragent():
    """
    useragent random setter
    """
    useragents = BeautifulSoup(
        requests.get(
            "https://developers.whatismybrowser.com/"
            "useragents/explore/operating_system_name/android/"
        ).content,
        "lxml",
    ).findAll("td", {"class": "useragent"})
    user_agent = choice(useragents)
    return user_agent.text


async def pbio(event):
    if event.fwd_from:
        return
    bio = event.pattern_match.group(1)
    try:
        await event.client(functions.account.UpdateProfileRequest(about=bio))
        await event.edit("Succesfully changed my profile bio")
    except Exception as e:
        await event.edit(str(e))


async def pname(event):
    if event.fwd_from:
        return
    names = event.pattern_match.group(1)
    first_name = names
    last_name = ""
    if "\\n" in names:
        first_name, last_name = names.split("\\n", 1)
    try:
        await event.client(
            functions.account.UpdateProfileRequest(
                first_name=first_name, last_name=last_name
            )
        )
        await event.edit("My name was changed successfully")
    except Exception as e:
        await event.edit(str(e))


async def anpfp(event):
    await event.edit(f"{r}")
    while True:
        await animepp()
        file = await event.client.upload_file("donottouch.jpg")
        await event.client(functions.photos.UploadProfilePhotoRequest(file))
        os.system("rm -rf donottouch.jpg")
        await asyncio.sleep(60)


async def avpfp(event):
    await event.edit(f"{s}")
    while True:
        await avengerspic()
        file = await event.client.upload_file("donottouch.jpg")
        await event.client(functions.photos.UploadProfilePhotoRequest(file))
        os.system("rm -rf donottouch.jpg")
        await asyncio.sleep(600)


async def gmpfp(event):
    await event.edit(f"{t}")
    while True:
        await gamerpic()
        file = await event.client.upload_file("donottouch.jpg")
        await event.client(functions.photos.UploadProfilePhotoRequest(file))
        os.system("rm -rf donottouch.jpg")
        await asyncio.sleep(60)


async def atnm(event):
    if event.fwd_from:
        return
    while True:
        dname = await pikaa(event, "ALIVE_NAME")
        DM = time.strftime("%d-%m-%y")
        HM = time.strftime("%H:%M")
        name = f"🕒{HM} ⚡{dname}⚡ 📅{DM}"
        logger.info(name)
        try:
            await event.client(functions.account.UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(DEL_TIME_OUT)
    await event.edit(f"Auto Name has been started Master")


async def atb(event):
    if event.fwd_from:
        return
    while True:
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        bio = f"📅 {DMY} | {DBIO} | ⌚️ {HM}"
        logger.info(bio)
        try:
            await event.client(functions.account.UpdateProfileRequest(about=bio))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(DEL_TIME_OUT)


async def _setgpic(gpic):
    """ For .setgpic command, changes the picture of a group """
    if not gpic.is_group:
        await gpic.edit("`I don't think this is a group.`")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        await gpic.edit(NO_ADMIN)
        return

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await gpic.edit(INVALID_MEDIA)

    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await gpic.client.upload_file(photo))
            )
            await gpic.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)


async def _promote(promt):
    """ For .promote command, promotes the replied/tagged person """
    # Get targeted chat
    chat = await promt.get_chat()
    # Grab admin status or creator in a chat
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, also return
    if not admin and not creator:
        await promt.edit(NO_ADMIN)
        return

    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )

    await promt.edit("`Promoting...`")
    user, rank = await get_user_from_event(promt)
    if not rank:
        # Just in case.
        rank = "admeme"
    if user:
        pass
    else:
        return

    # Try to promote if current user is admin or creator
    try:
        await promt.client(EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.edit("`Promoted Successfully!`")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        await promt.edit(NO_PERM)
        return

    # Announce to the logging group if we have promoted successfully
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID,
            "#PROMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {promt.chat.title}(`{promt.chat_id}`)",
        )


async def _demote(dmod):
    """ For .demote command, demotes the replied/tagged person """
    # Admin right check
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await dmod.edit(NO_ADMIN)
        return

    # If passing, declare that we're going to demote
    await dmod.edit("`Demoting...`")
    rank = "admeme"  # dummy rank, lol.
    user = await get_user_from_event(dmod)
    user = user[0]
    if user:
        pass
    else:
        return

    # New rights after demotion
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    # Edit Admin Permission
    try:
        await dmod.client(EditAdminRequest(dmod.chat_id, user.id, newrights, rank))

    # If we catch BadRequestError from Telethon
    # Assume we don't have permission to demote
    except BadRequestError:
        await dmod.edit(NO_PERM)
        return
    await dmod.edit("`Demoted Successfully!`")

    # Announce to the logging group if we have demoted successfully
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID,
            "#DEMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {dmod.chat.title}(`{dmod.chat_id}`)",
        )


async def _ban(bon):
    """ For .ban command, bans the replied/tagged person """
    # Here laying the sanity check
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await bon.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(bon)
    if user:
        pass
    else:
        return

    # Announce that we're going to whack the pest
    await bon.edit("`Whacking the pest!`")

    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        await bon.edit(NO_PERM)
        return
    # Helps ban group join spammers more easily
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await bon.edit("`I dont have message nuking rights! But still he was banned!`")
        return
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await bon.edit(
            f"{user.first_name} was banned !!\
        \nID: `{str(user.id)}`\
        \nReason: {reason}"
        )
    else:
        await bon.edit(
            f"{user.first_name} was banned !!\
        \nID: `{str(user.id)}`"
        )
    # Announce to the logging group if we have banned the person
    # successfully!
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID,
            "#BAN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {bon.chat.title}(`{bon.chat_id}`)",
        )


async def _unban(unbon):
    """ For .unban command, unbans the replied/tagged person """
    # Here laying the sanity check
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await unbon.edit(NO_ADMIN)
        return

    # If everything goes well...
    await unbon.edit("`Unbanning...`")

    user = await get_user_from_event(unbon)
    user = user[0]
    if user:
        pass
    else:
        return

    try:
        await unbon.client(EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.edit("```Unbanned Successfully```")

        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID,
                "#UNBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {unbon.chat.title}(`{unbon.chat_id}`)",
            )
    except UserIdInvalidError:
        await unbon.edit("`Uh oh my unban logic broke!`")


async def _mute(spdr):
    """
    This function is basically muting peeps
    """
    # Check if the function running under SQL mo
    pika = await spdr.client.get_me()
    try:
        from pikabot.sql_helper.spam_mute_sql import mute, mute2
    except AttributeError:
        await spdr.edit(NO_SQL)
        return

    # Admin or creator check
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await spdr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(spdr)
    if user:
        pass
    else:
        return

    self_user = await spdr.client.get_me()

    if user.id == self_user.id:
        await spdr.edit("`Hands too short, can't duct tape myself...\n(ヘ･_･)ヘ┳━┳`")
        return

    # If everything goes well, do announcing and mute
    await spdr.edit("`Gets a tape!`")
    if pika.id == pika_id1:
        pikamute = mute(spdr.chat_id, user.id)
    if pika.id == pika_id2:
        pikamute = mute2(spdr.chat_id, user.id)
    if pikamute is False:
        return await spdr.edit("`Error! User probably already muted.`")
    else:
        try:
            await spdr.client(EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))

            # Announce that the function is done
            if reason:
                await spdr.edit(f"`Safely taped !!`\nReason: {reason}")
            else:
                await spdr.edit("`Safely taped !!`")

            # Announce to logging group
            if BOTLOG:
                await spdr.client.send_message(
                    BOTLOG_CHATID,
                    "#MUTE\n"
                    f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                    f"CHAT: {spdr.chat.title}(`{spdr.chat_id}`)",
                )
        except UserIdInvalidError:
            return await spdr.edit("`Uh oh my mute logic broke!`")


async def _unmute(unmot):
    """ For .unmute command, unmute the replied/tagged person """
    # Admin or creator check
    pika = await unmot.client.get_me()
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await unmot.edit(NO_ADMIN)
        return

    # Check if the function running under SQL mode
    try:
        from pikabot.sql_helper.mute_sql import unmute, unmute2
    except AttributeError:
        await unmot.edit(NO_SQL)
        return

    # If admin or creator, inform the user and start unmuting
    await unmot.edit("```Unmuting...```")
    user = await get_user_from_event(unmot)
    user = user[0]
    if user:
        pass
    else:
        return
    if pika.id == pika_id1:
        pikaumute = unmute(unmot.chat_id, user.id)
    if pika.id == pika_id2:
        pikaumute = unmute2(unmot.chat_id, user.id)
    if pikaumute is False:
        return await unmot.edit("`Error! User probably already unmuted.`")
    else:

        try:
            await unmot.client(EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
            await unmot.edit("```Unmuted Successfully```")
        except UserIdInvalidError:
            await unmot.edit("`Uh oh my unmute logic broke!`")
            return

        if BOTLOG:
            await unmot.client.send_message(
                BOTLOG_CHATID,
                "#UNMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {unmot.chat.title}(`{unmot.chat_id}`)",
            )


async def _ungmute(un_gmute):
    """ For .ungmute command, ungmutes the target in the userbot """
    # Admin or creator check
    pika = await un_gmute.client.get_me()
    chat = await un_gmute.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await un_gmute.edit(NO_ADMIN)
        return

    # Check if the function running under SQL mode
    try:
        from pikabot.sql_helper.gmute_sql import ungmute, ungmute2
    except AttributeError:
        await un_gmute.edit(NO_SQL)
        return

    user = await get_user_from_event(un_gmute)
    user = user[0]
    if user:
        pass
    else:
        return

    # If pass, inform and start ungmuting
    await un_gmute.edit("```Ungmuting...```")

    if pika.id == pika_id1:
        pikaugmute = ungmute(unmot.chat_id, user.id)
    if pika.id == pika_id2:
        pikaugmute = ungmute2(unmot.chat_id, user.id)
    if pikaugmute is False:
        await un_gmute.edit("`Error! User probably not gmuted.`")
    else:
        # Inform about success
        await un_gmute.edit("```Ungmuted Successfully```")

        if BOTLOG:
            await un_gmute.client.send_message(
                BOTLOG_CHATID,
                "#UNGMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {un_gmute.chat.title}(`{un_gmute.chat_id}`)",
            )


async def _gmte(gspdr):
    """ For .gmute command, globally mutes the replied/tagged person """
    # Admin or creator check
    pika = await gspdr.client.get_me()
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await gspdr.edit(NO_ADMIN)
        return

    # Check if the function running under SQL mode
    try:
        from pikabot.sql_helper.gmute_sql import gmute, gmute2
    except AttributeError:
        await gspdr.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(gspdr)
    if user:
        pass
    else:
        return

    # If pass, inform and start gmuting
    await gspdr.edit("`Grabs a huge, sticky duct tape!`")

    if pika.id == pika_id1:
        pikagmute = gmute(unmot.chat_id, user.id)
    if pika.id == pika_id2:
        pikagmute = gmute2(unmot.chat_id, user.id)
    if pikagmute is False:
        await gspdr.edit("`Error! User probably already gmuted.\nRe-rolls the tape.`")
    else:
        if reason:
            await gspdr.edit(f"`Globally taped!`Reason: {reason}")
        else:
            await gspdr.edit("`Globally taped!`")

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID,
                "#GMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {gspdr.chat.title}(`{gspdr.chat_id}`)",
            )


async def _rmdacc(show):
    """ For .delusers command, list all the ghost/deleted accounts in a chat. """
    if not show.is_group:
        await show.edit("`I don't think this is a group.`")
        return
    con = show.pattern_match.group(1)
    del_u = 0
    del_status = "`No deleted accounts found, Group is cleaned as Hell`"

    if con != "clean":
        await show.edit("`Searching for zombie accounts...`")
        async for user in show.client.iter_participants(show.chat_id, aggressive=True):
            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = f"Found **{del_u}** deleted account(s) in this group,\
            \nclean them by using .delusers clean"

        await show.edit(del_status)
        return

    # Here laying the sanity check
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await show.edit("`I am not an admin here!`")
        return

    await show.edit("`Deleting deleted accounts...\nOh I can do that?!?!`")
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS)
                )
            except ChatAdminRequiredError:
                await show.edit("`I don't have ban rights in this group`")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await show.client(EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s)"

    if del_a > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s) \
        \n**{del_a}** deleted admin accounts are not removed"

    await show.edit(del_status)
    await sleep(2)
    await show.delete()

    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            "#CLEANUP\n"
            f"Cleaned **{del_u}** deleted account(s) !!\
            \nCHAT: {show.chat.title}(`{show.chat_id}`)",
        )


async def _gadmin(show):
    """ For .admins command, list all of the admins of the chat. """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f"<b>Admins in {title}:</b> \n"
    try:
        async for user in show.client.iter_participants(
            show.chat_id, filter=ChannelParticipantsAdmins
        ):
            if not user.deleted:
                link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nDeleted Account <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    await show.edit(mentions, parse_mode="html")


async def _pin(msg):
    """ For .pin command, pins the replied/tagged message on the top the chat. """
    # Admin or creator check
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await msg.edit(NO_ADMIN)
        return

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        await msg.edit("`Reply to a message to pin it.`")
        return

    options = msg.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        await msg.edit(NO_PERM)
        return

    await msg.edit("`Pinned Successfully!`")

    user = await get_user_sender_id(msg.sender_id, msg)

    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID,
            "#PIN\n"
            f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"LOUD: {not is_silent}",
        )


async def _kick(usr):
    """ For .kick command, kicks the replied/tagged person from the group. """
    # Admin or creator check
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await usr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(usr)
    if not user:
        await usr.edit("`Couldn't fetch user.`")
        return

    await usr.edit("`Kicking...`")

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        await usr.edit(NO_PERM + f"\n{str(e)}")
        return

    if reason:
        await usr.edit(
            f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`\nReason: {reason}"
        )
    else:
        await usr.edit(f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`")

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID,
            "#KICK\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {usr.chat.title}(`{usr.chat_id}`)\n",
        )


async def _gusers(show):
    """ For .users command, list all of the users in a chat. """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = "Users in {}: \n".format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                show.chat_id, search=f"{searchq}"
            ):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit("Damn, this is a huge group. Uploading users lists as file.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "userslist.txt",
            caption="Users in {}".format(title),
            reply_to=show.id,
        )
        remove("userslist.txt")

async def _muter(moot):
    """ Used for deleting the messages of muted people """
    pika=await moot.client.get_me()
    try:
        from pikabot.sql_helper._mute_sql import is_muted,is_muted2
        from pikabot.sql_helper.gmute_sql import is_gmuted,is_gmuted2
    except AttributeError:
        return
    if pika.id == pika_id1:
        muted = is_muted(moot.chat_id)
        gmuted = is_gmuted(moot.sender_id)
    if pika.id==pika_id2:
        muted = is_muted2(moot.chat_id)
        gmuted = is_gmuted2(moot.sender_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if str(i.sender) == str(moot.sender_id):
                try:
                    await moot.delete()
                    await moot.client(
                        EditBannedRequest(moot.chat_id, moot.sender_id,
                                          rights))
                except (BadRequestError, UserAdminInvalidError,
                        ChatAdminRequiredError, UserIdInvalidError):
                    await moot.client.send_read_acknowledge(
                        moot.chat_id, moot.id)
    if gmuted:
        for i in gmuted:
            if i.sender == str(moot.sender_id):
                try:
                    await moot.delete()
                except BadRequestError:
                    await moot.client.send_read_acknowledge(
                        moot.chat_id, moot.id)

async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit("`Pass the user's username, id or reply!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_user_sender_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None

    return user_obj


async def _alive(event):
    pupt = grt((time.time() - UpTime))
    try:
        pic = await pikaa(event, "ALIVE_PIC")
    except BaseException:
        pic = apic
    az = await pikaa(event, "ALIVE_NAME")
    await event.delete()
    a = await event.client.send_file(
        event.chat_id, pic, caption=alivestr.format(pupt, az)
    )
    await asyncio.sleep(15)
    await a.delete()


async def magisk(request):
    """ magisk latest releases """
    magisk_dict = {
        "Stable": "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/stable.json",
        "Beta": "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/beta.json",
        "Canary (Release)": "https://raw.githubusercontent.com/topjohnwu/magisk_files/canary/release.json",
        "Canary (Debug)": "https://raw.githubusercontent.com/topjohnwu/magisk_files/canary/debug.json",
    }
    releases = "Latest Magisk Releases:\n"
    for name, release_url in magisk_dict.items():
        data = get(release_url).json()
        releases += (
            f'{name}: [ZIP v{data["magisk"]["version"]}]({data["magisk"]["link"]}) | '
            f'[APK v{data["app"]["version"]}]({data["app"]["link"]}) | '
            f'[Uninstaller]({data["uninstaller"]["link"]})\n'
        )
    await request.edit(releases)


async def device_info(request):
    """ get android device basic info from its codename """
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text
    else:
        await request.edit("`Usage: .device <codename> / <model>`")
        return
    found = [
        i
        for i in get(DEVICES_DATA).json()
        if i["device"] == device or i["model"] == device
    ]
    if found:
        reply = f"Search results for {device}:\n\n"
        for item in found:
            brand = item["brand"]
            name = item["name"]
            codename = item["device"]
            model = item["model"]
            reply += (
                f"{brand} {name}\n"
                f"**Codename**: `{codename}`\n"
                f"**Model**: {model}\n\n"
            )
    else:
        reply = f"`Couldn't find info about {device}!`\n"
    await request.edit(reply)


async def codename_info(request):
    """ search for android codename """
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        await request.edit("`Usage: .codename <brand> <device>`")
        return
    found = [
        i
        for i in get(DEVICES_DATA).json()
        if i["brand"].lower() == brand and device in i["name"].lower()
    ]
    if len(found) > 8:
        found = found[:8]
    if found:
        reply = f"Search results for {brand.capitalize()} {device.capitalize()}:\n\n"
        for item in found:
            brand = item["brand"]
            name = item["name"]
            codename = item["device"]
            model = item["model"]
            reply += (
                f"{brand} {name}\n"
                f"**Codename**: `{codename}`\n"
                f"**Model**: {model}\n\n"
            )
    else:
        reply = f"`Couldn't find {device} codename!`\n"
    await request.edit(reply)


async def dspecs(request):
    """ Mobile devices specifications """
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        await request.edit("`Usage: .specs <brand> <device>`")
        return
    all_brands = (
        BeautifulSoup(
            get("https://www.devicespecifications.com/en/brand-more").content, "lxml"
        )
        .find("div", {"class": "brand-listing-container-news"})
        .findAll("a")
    )
    brand_page_url = None
    try:
        brand_page_url = [
            i["href"] for i in all_brands if brand == i.text.strip().lower()
        ][0]
    except IndexError:
        await request.edit(f"`{brand} is unknown brand!`")
    devices = BeautifulSoup(get(brand_page_url).content, "lxml").findAll(
        "div", {"class": "model-listing-container-80"}
    )
    device_page_url = None
    try:
        device_page_url = [
            i.a["href"]
            for i in BeautifulSoup(str(devices), "lxml").findAll("h3")
            if device in i.text.strip().lower()
        ]
    except IndexError:
        await request.edit(f"`can't find {device}!`")
    if len(device_page_url) > 2:
        device_page_url = device_page_url[:2]
    reply = ""
    for url in device_page_url:
        info = BeautifulSoup(get(url).content, "lxml")
        reply = "\n**" + info.title.text.split("-")[0].strip() + "**\n\n"
        info = info.find("div", {"id": "model-brief-specifications"})
        specifications = re.findall(r"<b>.*?<br/>", str(info))
        for item in specifications:
            title = re.findall(r"<b>(.*?)</b>", item)[0].strip()
            data = (
                re.findall(r"</b>: (.*?)<br/>", item)[0]
                .replace("<b>", "")
                .replace("</b>", "")
                .strip()
            )
            reply += f"**{title}**: {data}\n"
    await request.edit(reply)


async def twrp(request):
    """ get android device twrp """
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(" ")[0]
    else:
        await request.edit("`Usage: .twrp <codename>`")
        return
    url = get(f"https://dl.twrp.me/{device}/")
    if url.status_code == 404:
        reply = f"`Couldn't find twrp downloads for {device}!`\n"
        await request.edit(reply)
        return
    page = BeautifulSoup(url.content, "lxml")
    download = page.find("table").find("tr").find("a")
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = (
        f"**Latest TWRP for {device}:**\n"
        f"[{dl_file}]({dl_link}) - __{size}__\n"
        f"**Updated:** __{date}__\n"
    )
    await request.edit(reply)


async def waifu(animu):
    # """Creates random anime sticker!"""

    text = animu.pattern_match.group(1)
    if not text:
        if animu.is_reply:
            text = (await animu.get_reply_message()).message
        else:
            await animu.edit("You haven't written any article, Waifu is going away.")
            return
    animus = [1, 3, 7, 9, 13, 22, 34, 35, 36, 37, 43, 44, 45, 52, 53, 55]
    sticcers = await animu.client.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(text))}"
    )
    await sticcers[0].click(
        animu.chat_id,
        reply_to=animu.reply_to_msg_id,
        silent=True if animu.is_reply else False,
        hide_via=True,
    )
    await animu.delete()


async def _bash(event):
    if event.fwd_from:
        return
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    o = stdout.decode()
    if not o:
        o = "**Tip**: \n`If you want to see the results of your code, I suggest printing them to stdout.`"
    else:
        _o = o.split("\n")
        o = "`\n".join(_o)
    OUTPUT = f"**Qᴜᴇʀʏ:**\n**Cᴏᴍᴍᴀɴᴅ:**\n`{cmd}` \n**Pɪᴅ**\n`{process.pid}`\n\n**Sᴛᴅᴇʀʀ:** \n`{e}`\n**Oᴜᴛᴘᴜᴛ:**\n{o}"
    if len(OUTPUT) > 4095:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "exec.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id,
            )
            await event.delete()
    await event.edit(OUTPUT)


async def batch_upload(event):
    if event.fwd_from:
        return
    temp_dir = Config.TEMP_DIR
    if os.path.exists(temp_dir):
        files = sorted(os.listdir(temp_dir))
        await event.edit("Uploading Files on Telegram...")
        for file in files:
            required_file_name = temp_dir + "/" + file
            print(required_file_name)
            await event.client.send_file(
                event.chat_id, required_file_name, force_document=True
            )
    else:
        await event.edit("Directory Not Found.")
        return
    await event.edit("Successfull.")


async def belo(event):

    if event.fwd_from:

        return

    await event.edit("Typing...")

    await asyncio.sleep(2)

    x = random.randrange(1, 96)

    if x == 1:

        await event.edit(
            '`"Underwater bubbles and raindrops are total opposites of each other."`'
        )

    if x == 2:

        await event.edit(
            '`"If you buy an eraser you are literally paying for your mistakes."`'
        )

    if x == 3:

        await event.edit(
            '`"The Person you care for most has the potential to destroy you the most."`'
        )

    if x == 4:

        await event.edit(
            '`"If humans colonize the moon, it will probably attract retirement homes as the weaker gravity will allow the elderly to feel stronger."`'
        )

    if x == 5:

        await event.edit(
            '`"Any video with “wait for it” in the title is simply too long."`'
        )

    if x == 6:

        await event.edit(
            '`"Your age in years is how many times you’ve circled the Sun, but your age in months is how many times the Moon has circled you."`'
        )

    if x == 7:

        await event.edit(
            '`"Biting your tongue while eating is a perfect example of how you can still screw up, even with decades of experience."`'
        )

    if x == 8:

        await event.edit(
            '`"Saying that your home is powered by a wireless Nuclear fusion reactor that is 93 Million miles away sounds way cooler than just saying you have solar panels on your roof."`'
        )

    if x == 9:

        await event.edit(
            '`"The most crushing feeling is when someone smiles at you on the street and you don’t react fast enough to smile back."`'
        )

    if x == 10:

        await event.edit(
            '`"Teeth constantly require maintenance to prevent their decay when alive, and yet they manage to survive for thousands of years buried as fossils."`'
        )

    if x == 11:

        await event.edit('`"A folder is for things that you don\'t want to fold."`')

    if x == 12:

        await event.edit(
            '`"Waking up in the morning sometimes feels like resuming a shitty movie you decided to quit watching."`'
        )

    if x == 13:

        await event.edit(
            '`"If everything goes seventhly, you probably won\'t remember today."`'
        )

    if x == 14:

        await event.edit(
            '`"When you meet new people in real life, you unlock more characters for your dream world."`'
        )

    if x == 15:

        await event.edit(
            '`"Maybe if they renamed sunscreen to “anti-cancer cream” more people would wear it."`'
        )

    if x == 16:

        await event.edit(
            '`"200 years ago, people would never have guessed that humans in the future would communicate by silently tapping on glass."`'
        )

    if x == 17:

        await event.edit(
            '`"Parents worry about what their sons download and worry about what their daughters upload."`'
        )

    if x == 18:

        await event.edit(
            '`"It\'s crazy how you can be the same age as someone, but at a completely different stage in your life."`'
        )

    if x == 19:

        await event.edit(
            "`\"When you think you wanna die, you really don't wanna die, you just don't wanna live like this.\"`"
        )

    if x == 20:

        await event.edit('`"Technically, no one has ever been in an empty room."`')

    if x == 21:

        await event.edit(
            '`"An onion is the bass player of food. You would probably not enjoy it solo, but you’d miss it if it wasn’t there."`'
        )

    if x == 22:

        await event.edit(
            "`\"We run everywhere in videogames because we're too lazy to walk, but In real life we walk everywhere because we're too lazy to run.\"`"
        )

    if x == 23:

        await event.edit(
            '`"Every single decision you ever made has brought you to read this sentence."`'
        )

    if x == 24:

        await event.edit("`\"The word 'quiet' is often said very loud.\"`")

    if x == 25:

        await event.edit(
            '`"Everybody wants you to work hard, but nobody wants to hear about how hard you work."`'
        )

    if x == 26:

        await event.edit(
            '`"We brush our teeth with hair on a stick and brush our hair with teeth on a stick."`'
        )

    if x == 27:

        await event.edit(
            '`"No one remembers your awkward moments but they’re too busy remembering their own."`'
        )

    if x == 28:

        await event.edit(
            '`"Dumb people try to say simple ideas as complex as possible while smart people try to say complex ideas as simple as possible."`'
        )

    if x == 29:

        await event.edit(
            "`\"Some people think they're better than you because they grew up richer. Some people think they're better than you because they grew up poorer.\"`"
        )

    if x == 30:

        await event.edit(
            '`"The biggest irony is that computers & mobiles were invented to save out time!"`'
        )

    if x == 31:

        await event.edit(
            '`"After honey was first discovered, there was likely a period where people were taste testing any available slime from insects."`'
        )

    if x == 32:

        await event.edit(
            '`"You know you’re getting old when your parents start disappointing you, instead of you disappointing them."`'
        )

    if x == 33:

        await event.edit(
            '`"Humans are designed to learn through experience yet the education system has made it so we get no experience."`'
        )

    if x == 34:

        await event.edit(
            '`"By focusing on blinking, you blink slower... Same for breathing."`'
        )

    if x == 35:

        await event.edit(
            '`"Drivers in a hurry to beat traffic usually cause the accidents which create the traffic they were trying to avoid."`'
        )

    if x == 36:

        await event.edit(
            '`"Characters that get married in fiction were literally made for each other."`'
        )

    if x == 37:

        await event.edit(
            '`"Babies are a clean hard drive that can be programmed with any language."`'
        )

    if x == 38:

        await event.edit(
            "`\"There could be a miracle drug that cures every disease to man, that we'll never know about because it doesn't work on rats.\"`"
        )

    if x == 39:

        await event.edit(
            "`\"Rhinos evolved to grow a horn for protection, but it's what's making them go extinct.\"`"
        )

    if x == 40:

        await event.edit(
            '`"Maybe we don\'t find time travelers because we all die in 25-50 years."`'
        )

    if x == 41:

        await event.edit(
            '`"Sleep is the trial version of death, It even comes with ads based on your activity."`'
        )

    if x == 42:

        await event.edit(
            '`"The most unrealistic thing about Spy movies is how clean the air ventilation system is!"`'
        )

    if x == 43:

        await event.edit(
            '`"In games we play through easy modes to unlock hard modes. In life we play through hard modes to unlock easy modes."`'
        )

    if x == 44:

        await event.edit(
            '`"Silent people seem smarter than loud people, because they keep their stupid thoughts to themselves."`'
        )

    if x == 45:

        await event.edit('`"If Greenland actually turns green, we\'re all screwed."`')

    if x == 46:

        await event.edit(
            '`"If someone says clever things in your dream, it actually shows your own cleverness."`'
        )

    if x == 47:

        await event.edit(
            '`"Famous movie quotes are credited to the actor and not the actual writer who wrote them."`'
        )

    if x == 48:

        await event.edit(
            '`"No one actually teaches you how to ride a bicycle. They just hype you up until you work it out."`'
        )

    if x == 49:

        await event.edit('`"Ask yourself why the the brain ignores the second the."`')

    if x == 50:

        await event.edit(
            '`"You’ve probably forgot about 80% of your entire life and most of the memories you do remember are not very accurate to what actually happened."`'
        )

    if x == 51:

        await event.edit(
            '`"It will be a lot harder for kids to win against their parents in video games in the future."`'
        )

    if x == 52:

        await event.edit(
            '`"Everyone has flaws, if you don\'t recognize yours, you have a new one."`'
        )

    if x == 53:

        await event.edit('`"Raising a child is training your replacement."`')

    if x == 54:

        await event.edit(
            "`\"'O'pen starts with a Closed circle, and 'C'lose starts with an open circle.\"`"
        )

    if x == 55:

        await event.edit(
            '`"There\'s always someone who hated you for no reason, and still does."`'
        )

    if x == 56:

        await event.edit(
            '`"After popcorn was discovered, there must have been a lot of random seeds that were roasted to see if it would have the same effect."`'
        )

    if x == 57:

        await event.edit(
            '`"The more important a good night\'s sleep is, the harder it is to fall asleep."`'
        )

    if x == 58:

        await event.edit(
            '`"Blessed are those that can properly describe the type of haircut they want to a new stylist."`'
        )

    if x == 59:

        await event.edit(
            "`\"Too many people spend money they haven't earned, to buy things they don't want, to impress people they don't like!\"`"
        )

    if x == 60:

        await event.edit(
            '`"Theme park employees must be good at telling the difference between screams of horror and excitement."`'
        )

    if x == 61:

        await event.edit('`"6 to 6:30 feels more half-an-hour than 5:50 to 6:20"`')

    if x == 62:

        await event.edit(
            '`"Getting your password right on the last login attempt before lockout is the closest thing to disarming a bomb at the last minute that most of us will experience."`'
        )

    if x == 63:

        await event.edit(
            '`"Listening to podcasts before bed is the adult version of story-time."`'
        )

    if x == 64:

        await event.edit(
            '`"If all criminals stopped robbing then the security industry would fall in which they could then easily go back to robbing."`'
        )

    if x == 65:

        await event.edit('`"A ton of whales is really only like half a whale."`')

    if x == 66:

        await event.edit(
            '`"When you get old, the old you is technically the new you, and your young self is the old you."`'
        )

    if x == 67:

        await event.edit(
            '`"You probably won\'t find many negative reviews of parachutes on the Internet."`'
        )

    if x == 68:

        await event.edit(
            '`"We show the most love and admiration for people when they\'re no longer around to appreciate it."`'
        )

    if x == 69:

        await event.edit(
            "`\"We've practiced sleeping thousands of times, yet can't do it very well or be consistent.\"`"
        )

    if x == 70:

        await event.edit(
            '`"Humans are more enthusiastic about moving to another planet with hostile environment than preserving earth - the planet they are perfectly shaped for."`'
        )

    if x == 71:

        await event.edit(
            "`\"The happiest stage of most people's lives is when their brains aren't fully developed yet.\"`"
        )

    if x == 72:

        await event.edit('`"The most effective alarm clock is a full bladder."`')

    if x == 73:

        await event.edit(
            '`"You probably just synchronized blinks with millions of people."`'
        )

    if x == 74:

        await event.edit(
            '`"Since we test drugs on animals first, rat medicine must be years ahead of human medicine."`'
        )

    if x == 75:

        await event.edit(
            '`"Night before a day off is more satisfying than the actual day off."`'
        )

    if x == 76:

        await event.edit('`"We put paper in a folder to keep it from folding."`')

    if x == 77:

        await event.edit(
            '`"Somewhere, two best friends are meeting for the first time."`'
        )

    if x == 78:

        await event.edit(
            '`"Our brain simultaneously hates us, loves us, doesn\'t care about us, and micromanages our every move."`'
        )

    if x == 79:

        await event.edit(
            '`"Being a male is a matter of birth. Being a man is a matter of age. But being a gentleman is a matter of choice."`'
        )

    if x == 80:

        await event.edit(
            '`"Soon the parents will be hiding their social account from their kids rather than kids hiding their accounts from the parents."`'
        )

    if x == 81:

        await event.edit('`"Wikipedia is what the internet was meant to be."`')

    if x == 82:

        await event.edit(
            '`"A theme park is the only place that you can hear screams in the distance and not be concerned."`'
        )

    if x == 83:

        await event.edit(
            '`"A wireless phone charger offers less freedom of movement than a wired one."`'
        )

    if x == 84:

        await event.edit(
            "`\"If you repeatedly criticize someone for liking something you don't, they won't stop liking it. They'll stop liking you.\"`"
        )

    if x == 85:

        await event.edit(
            '`"Somewhere there is a grandmother, whose grandson really is the most handsome boy in the world."`'
        )

    if x == 86:

        await event.edit(
            '`"If someday human teleportation becomes real, people will still be late for work."`'
        )

    if x == 87:

        await event.edit(
            '`"The first humans who ate crabs must have been really hungry to try and eat an armored sea spider"`'
        )

    if x == 88:

        await event.edit(
            '`"Doing something alone is kind of sad, but doing it solo is cool af."`'
        )

    if x == 89:

        await event.edit(
            '`"Your brain suddenly becomes perfect at proofreading after you post something."`'
        )

    if x == 90:

        await event.edit(
            '`"There\'s always that one song in your playlist that you always skip but never remove."`'
        )

    if x == 91:

        await event.edit(
            '`"Kids next century will probably hate us for taking all the good usernames."`'
        )

    if x == 92:

        await event.edit('`"Bubbles are to fish what rain is to humans."`')

    if x == 93:

        await event.edit(
            '`"The more people you meet, the more you realise and appreciate how well your parents raised you."`'
        )

    if x == 94:

        await event.edit('`"A comma is a short pause, a coma is a long pause."`')

    if x == 95:

        await event.edit('`"Someday you will either not wake up or not go to sleep."`')

    if x == 96:

        await event.edit(
            '`"Bermuda Triangle might be the exit portal of this simulation."`'
        )

    if x == 97:

        await event.edit(
            '`"If we put solar panels above parking lots, then our cars wouldn\'t get hot and we would have a lot of clean energy."`'
        )


async def bombs(event):
    if event.fwd_from:
        return
    await event.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await event.edit("💣💣💣💣 \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await event.edit("▪️▪️▪️▪️ \n💣💣💣💣 \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await event.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💣💣💣💣 \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await event.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💣💣💣💣 \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await event.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💣💣💣💣 \n")
    await asyncio.sleep(1)
    await event.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💥💥💥💥 \n")
    await asyncio.sleep(0.5)
    await event.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💥💥💥💥 \n💥💥💥💥 \n")
    await asyncio.sleep(0.5)
    await event.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n😵😵😵😵 \n")
    await asyncio.sleep(0.5)
    await event.edit("`RIP PLOXXX......`")
    await asyncio.sleep(2)


async def call(event):
    if event.fwd_from:
        return
    an = await pikaa(event, "ALIVE_NAME")
    animation_interval = 3
    animation_ttl = range(0, 18)
    await event.edit("Calling")
    animation_chars = [
        "`Connecting To Telegram Headquarters...`",
        "`Call Connected.`",
        "`Telegram: Hello This is Telegram HQ. Who is this?`",
        f"`Me: Yo this is **{an}**,`Please Connect me to my idiot bro,Ayush Durov`",
        "`User Authorised.`",
        "`Calling Pavel Durov`  `At +916969696969`",
        "`Private  Call Connected...`",
        "`Me: Hello Sir, Please Ban This Telegram Account.`",
        "`Pavel: May I Know Who Is This?`",
        f"`Me: Yo Brah, I Am`**{an}**",
        "`Pavel: OMG!!! Long time no see, Wassup Brother...\nI'll Make Sure That Guy Account Will Get Blocked Within 24Hrs.`",
        "`Me: Thanks, See You Later Brah.`",
        "`Pavel: Please Don't Thank Brah, Telegram Is Our's. Just Gimme A Call When You Become Free.`",
        "`Me: Is There Any Issue/Emergency???`",
        "`Pavel: Yes Sur, There Is A Bug In Telegram v69.6.9.\nI Am Not Able To Fix It. If Possible, Please Help Fix The Bug.`",
        "`Me: Send Me The App On My Telegram Account, I Will Fix The Bug & Send You.`",
        "`Pavel: Sure Sur \nTC Bye Bye :)`",
        "`Private Call Disconnected.`",
    ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 18])


async def spm_notify(event):
    if event.fwd_from:
        return
    mentions = "@admin: **Spam Spotted**"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(
        chat, filter=ChannelParticipantsAdmins
    ):
        mentions += f"[\u2063](tg://user?id={x.id})"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


async def _carbon(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@"):
        """ A Wrapper for carbon.now.sh """
        await e.edit("`Processing..`")
        CARBON = "https://carbon.now.sh/?l={lang}&code={code}"
        global CARBONLANG
        textx = await e.get_reply_message()
        pcode = e.text
        if pcode[8:]:
            pcode = str(pcode[8:])
        elif textx:
            pcode = str(textx.message)

        code = quote_plus(pcode)
        await e.edit("`Meking Carbon...\n25%`")
        url = CARBON.format(code=code, lang=CARBONLANG)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = GOOGLE_CHROME_BIN
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        prefs = {"download.default_directory": "./"}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER, options=chrome_options)
        driver.get(url)
        await e.edit("`Be Patient...\n50%`")
        download_path = "./"
        driver.command_executor._commands["send_command"] = (
            "POST",
            "/session/$sessionId/chromium/send_command",
        )
        params = {
            "cmd": "Page.setDownloadBehavior",
            "params": {"behavior": "allow", "downloadPath": download_path},
        }
        driver.execute("send_command", params)
        driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
        await e.edit("`Processing..\n75%`")
        sleep(1)
        await e.edit("`Done Dana Done...\n100%`")
        file = "./carbon.png"
        await e.edit("`Uploading..`")
        await e.client.send_file(
            e.chat_id,
            file,
            caption="<< Here's your carbon, \n Carbonised by [PikaBot](t.me/PikachuUserBot)>> ",
            force_document=True,
            reply_to=e.message.reply_to_msg_id,
        )
        os.remove("./carbon.png")
        driver.quit()
        await e.delete()  # Deleting msg


async def _chain(event):
    await event.edit("Counting...")
    count = -1
    message = event.message
    while message:
        reply = await message.get_reply_message()
        if reply is None:
            await event.client(
                SaveDraftRequest(
                    await event.get_input_chat(), "", reply_to_msg_id=message.id
                )
            )
        message = reply
        count += 1
    await event.edit(f"Chain length: {count}")


async def get_media(event):
    if event.fwd_from:
        return
    dir = "./temp/"
    try:
        os.makedirs("./temp/")
    except BaseException:
        pass
    channel_username = event.text
    limit = channel_username[6:9]
    print(limit)
    channel_username = channel_username[11:]
    print(channel_username)
    await event.edit("Downloading Media From this Channel.")
    msgs = await event.client.get_messages(channel_username, limit=int(limit))
    with open("log.txt", "w") as f:
        f.write(str(msgs))
    for msg in msgs:
        if msg.media is not None:
            await event.client.download_media(msg, dir)
    ps = subprocess.Popen(("ls", "temp"), stdout=subprocess.PIPE)
    output = subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", "")
    output = output.replace("\n'", "")
    await event.edit("Downloaded " + output + " files.")


async def getmedia(event):
    if event.fwd_from:
        return
    dir = "./temp/"
    try:
        os.makedirs("./temp/")
    except BaseException:
        pass
    channel_username = event.text
    channel_username = channel_username[7:]

    print(channel_username)
    await event.edit("Downloading All Media From this Channel.")
    msgs = await event.client.get_messages(channel_username, limit=3000)
    with open("log.txt", "w") as f:
        f.write(str(msgs))
    for msg in msgs:
        if msg.media is not None:
            await event.client.download_media(msg, dir)
    ps = subprocess.Popen(("ls", "temp"), stdout=subprocess.PIPE)
    output = subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", "")
    output = output.replace("\n'", "")
    await event.edit("Downloaded " + output + " files.")


async def _ctg(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("```Reply to a Link.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit("```Reply to a Link```")
        return
    chat = "@chotamreaderbot"
    reply_message.sender
    await event.edit("```Processing```")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=272572121)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("`RIP Check Your Blacklist Boss`")
            return
        if response.text.startswith(""):
            await event.edit("Am I Dumb Or Am I Dumb?")
        else:
            await event.delete()
            await event.client.send_message(event.chat_id, response.message)


async def cflip(event):
    if event.fwd_from:
        return
    r = random.randint(1, 100)
    input_str = event.pattern_match.group(1)
    if input_str:
        input_str = input_str.lower()
    if r % 2 == 1:
        if input_str == "heads":
            await event.edit("The coin landed on: **Heads**. \n You were correct.")
        elif input_str == "tails":
            await event.edit(
                "The coin landed on: **Heads**. \n You weren't correct, try again ..."
            )
        else:
            await event.edit("The coin landed on: **Heads**.")
    elif r % 2 == 0:
        if input_str == "tails":
            await event.edit("The coin landed on: **Tails**. \n You were correct.")
        elif input_str == "heads":
            await event.edit(
                "The coin landed on: **Tails**. \n You weren't correct, try again ..."
            )
        else:
            await event.edit("The coin landed on: **Tails**.")
    else:
        await event.edit(r"¯\_(ツ)_/¯")


async def findcolour(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
    if input_str.startswith("#"):
        try:
            usercolor = ImageColor.getrgb(input_str)
        except Exception as e:
            await event.edit(str(e))
            return False
        else:
            im = Image.new(mode="RGB", size=(1280, 720), color=usercolor)
            im.save("UniBorg.png", "PNG")
            input_str = input_str.replace("#", "#COLOR_")
            await event.client.send_file(
                event.chat_id,
                "PikaBot.png",
                force_document=False,
                caption=input_str,
                reply_to=message_id,
            )
            os.remove("PikaBot.png")
            await event.delete()
    else:
        await event.edit("Syntax: `.color <color_code>`")


async def _congo(event):
    if event.fwd_from:
        return
    bro = random.randint(0, len(CongoStr) - 1)
    reply_text = CongoStr[bro]
    await event.edit(reply_text)


async def _convoqt(event):
    if event.fwd_from:
        return
    await event.edit("selecting question...")
    await asyncio.sleep(2)
    x = random.randrange(1, 60)

    if x == 1:
        await event.edit(
            '`"Arrange them in descending order of importance – MONEY, LOVE, FAMILY, CAREER, FRIENDS."`'
        )

    if x == 2:

        await event.edit(
            '`"If you had to change your name, what would your new name be, and why would you choose that name?"`'
        )

    if x == 3:

        await event.edit(
            '`"What’s the most interesting thing you’ve read or seen this week?"`'
        )

    if x == 4:

        await event.edit('`"What scene from a TV show will you never forget?"`')

    if x == 5:

        await event.edit(
            '`"If you could become a master in one skill, what skill would you choose?"`'
        )

    if x == 6:

        await event.edit('`"What three words can describe you?"`')

    if x == 7:

        await event.edit(
            '`"If you had to delete one app from your phone, what would it be?"`'
        )

    if x == 8:

        await event.edit(
            '`"Would you go out with me if I was the last person on earth?"`'
        )

    if x == 9:

        await event.edit('`"If you switched genders for the day, what would you do?"`')

    if x == 10:

        await event.edit(
            '`"If you could eat lunch with someone here. Who would you choose?"`'
        )

    if x == 11:

        await event.edit(
            '`"If you were told you only had one week left to live, what would you do?"`'
        )

    if x == 12:

        await event.edit(
            '`"What\'s number one item you would save from your burning house?"`'
        )

    if x == 13:

        await event.edit(
            '`"If you could only text one person for the rest of your life, but you could never talk to that person face to face, who would that be?"`'
        )

    if x == 14:

        await event.edit('`"How many kids do you want to have in the future?"`')

    if x == 15:

        await event.edit(
            '`"Who in this group would be the worst person to date? Why?"`'
        )

    if x == 16:

        await event.edit('`"What does your dream boy or girl look like?"`')

    if x == 17:

        await event.edit(
            '`"What would be in your web history that you’d be embarrassed if someone saw?"`'
        )

    if x == 18:

        await event.edit('`"Do you sing in the shower?"`')

    if x == 19:

        await event.edit('`"What’s the right age to get married?"`')

    if x == 20:

        await event.edit('`"What are your top 5 rules for life?"`')

    if x == 21:

        await event.edit(
            '`"If given an option, would you choose a holiday at the beach or in the mountains?"`'
        )

    if x == 22:

        await event.edit(
            '`"If you are made the president of your country, what would be the first thing that you will do?"`'
        )

    if x == 23:

        await event.edit(
            '`"If given a chance to meet 3 most famous people on the earth, who would it be, answer in order of preference."`'
        )

    if x == 24:

        await event.edit(
            '`"Have you ever wished to have a superpower, if so, what superpower you would like to have?"`'
        )

    if x == 25:

        await event.edit(
            '`"Can you spend an entire day without phone and internet? If yes, what would you do?"`'
        )

    if x == 26:

        await event.edit('`"Live-in relation or marriage, what do you prefer?"`')

    if x == 27:

        await event.edit('`"What is your favorite cuisine or type of food?"`')

    if x == 28:

        await event.edit(
            '`"What are some good and bad things about the education system in your country?"`'
        )

    if x == 29:

        await event.edit('`"What do you think of online education?"`')

    if x == 30:

        await event.edit('`"What are some goals you have failed to accomplish?"`')

    if x == 31:

        await event.edit('`"Will technology save the human race or destroy it?"`')

    if x == 32:

        await event.edit('`"What was the best invention of the last 50 years?"`')

    if x == 33:

        await event.edit(
            '`"Have you travelled to any different countries? Which ones?"`'
        )

    if x == 34:

        await event.edit(
            '`"Which sport is the most exciting to watch? Which is the most boring to watch?"`'
        )

    if x == 35:

        await event.edit('`"What’s the most addictive mobile game you have played?"`')

    if x == 36:

        await event.edit('`"How many apps do you have on your phone?"`')

    if x == 37:

        await event.edit('`"What was the last song you listened to?"`')

    if x == 38:

        await event.edit(
            '`"Do you prefer to watch movies in the theater or in the comfort of your own home?"`'
        )

    if x == 39:

        await event.edit('`"Do you like horror movies? Why or why not?"`')

    if x == 40:

        await event.edit(
            '`"How often do you help others? Who do you help? How do you help?"`'
        )

    if x == 41:

        await event.edit('`"What song do you play most often?"`')

    if x == 42:

        await event.edit('`"Suggest a new rule that should be added in this group!"`')

    if x == 43:

        await event.edit('`"What app on your phone do you think I should get?"`')

    if x == 44:

        await event.edit(
            '`"What website or app has completely changed your life for better or for worse?"`'
        )

    if x == 45:

        await event.edit('`"What isn’t real but you desperately wish it was?"`')

    if x == 46:

        await event.edit('`"What thing do you really wish you could buy right now?"`')

    if x == 47:

        await event.edit(
            '`"If you could ban an admin from this group. Who would you prefer ?"`'
        )

    if x == 48:

        await event.edit(
            '`"What would you do if someone left a duffle bag filled with $2,000,000 on your back porch?"`'
        )

    if x == 49:

        await event.edit('`"Who is the luckiest person you know?"`')

    if x == 50:

        await event.edit(
            '`"If you could visit someone\'s house in this group, who would it be ?"`'
        )

    if x == 51:

        await event.edit('`"What are you tired of hearing about?"`')

    if x == 52:

        await event.edit(
            '`"If you died today, what would your greatest achievement be?"`'
        )

    if x == 53:

        await event.edit('`"What method will you choose to kill yourself?"`')

    if x == 54:

        await event.edit('`"What’s the best news you\'ve heard in the last 24 hours?"`')

    if x == 55:

        await event.edit(
            '`"What is the most important change that should be made to your country’s education system?"`'
        )

    if x == 56:

        await event.edit('`"Send your favourite sticker pack."`')

    if x == 57:

        await event.edit('`"Send your favourite animated sticker pack."`')

    if x == 58:

        await event.edit('`"Send your favourite video or gif."`')

    if x == 59:

        await event.edit('`"Send your favourite emojies"`')

    if x == 60:

        await event.edit(
            '`"What’s something you misunderstood as a child and only realized much later was wrong?"`'
        )


async def decide(event):
    if event.fwd_from:
        return
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
    r = requests.get("https://yesno.wtf/api").json()
    await event.client.send_message(
        event.chat_id, r["answer"], reply_to=message_id, file=r["image"]
    )
    await event.delete()


async def _cry(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 103)
    await event.edit("crying")
    animation_chars = [
        ";__",
        ";___",
        ";____",
        ";_____",
        ";______",
        ";_______",
        ";________",
        ";__________",
        ";____________",
        ";______________",
        ";________________",
        ";__________________",
        ";____________________",
        ";______________________",
        ";________________________",
        ";_________________________",
        ";_________________________",
        ";________________________",
        ";_______________________",
        ";______________________",
        ";_____________________",
        ";____________________",
        ";___________________",
        ";__________________",
        ";_________________",
        ";________________",
        ";_______________",
        ";_____________",
        ";___________",
        ";_________",
        ";_______",
        ";_____",
        ";____",
        ";___",
        ";__",
        ";You made me `CRY`",
    ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 35])


async def deepfryer(event):
    try:
        frycount = int(event.pattern_match.group(1))
        if frycount < 1:
            raise ValueError
    except ValueError:
        frycount = 1

    if event.is_reply:
        reply_message = await event.get_reply_message()
        data = await check_media(reply_message)

        if isinstance(data, bool):
            await event.edit("`I can't deep fry that!`")
            return
    else:
        await event.edit("`Reply to an image or sticker to deep fry it!`")
        return

    # download last photo (highres) as byte array
    await event.edit("`Downloading media…`")
    image = io.BytesIO()
    await event.client.download_media(data, image)
    image = Image.open(image)

    # fry the image
    await event.edit("`Deep frying media…`")
    for _ in range(frycount):
        image = await deepfry(image)

    fried_io = io.BytesIO()
    fried_io.name = "image.jpeg"
    image.save(fried_io, "JPEG")
    fried_io.seek(0)

    await event.reply(file=fried_io)


async def deepfry(img: Image) -> Image:
    colours = (
        (randint(50, 200), randint(40, 170), randint(40, 190)),
        (randint(190, 255), randint(170, 240), randint(180, 250)),
    )

    img = img.copy().convert("RGB")

    # Crush image to hell and back
    img = img.convert("RGB")
    width, height = img.width, img.height
    img = img.resize(
        (int(width ** uniform(0.8, 0.9)), int(height ** uniform(0.8, 0.9))),
        resample=Image.LANCZOS,
    )
    img = img.resize(
        (int(width ** uniform(0.85, 0.95)), int(height ** uniform(0.85, 0.95))),
        resample=Image.BILINEAR,
    )
    img = img.resize(
        (int(width ** uniform(0.89, 0.98)), int(height ** uniform(0.89, 0.98))),
        resample=Image.BICUBIC,
    )
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, randint(3, 7))

    # Generate colour overlay
    overlay = img.split()[0]
    overlay = ImageEnhance.Contrast(overlay).enhance(uniform(1.0, 2.0))
    overlay = ImageEnhance.Brightness(overlay).enhance(uniform(1.0, 2.0))

    overlay = ImageOps.colorize(overlay, colours[0], colours[1])

    # Overlay red and yellow onto main image and sharpen the hell out of it
    img = Image.blend(img, overlay, uniform(0.1, 0.4))
    img = ImageEnhance.Sharpness(img).enhance(randint(5, 300))

    return img


async def check_media(reply_message):
    if reply_message and reply_message.media:
        if reply_message.photo:
            data = reply_message.photo
        elif reply_message.document:
            if (
                DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
                in reply_message.media.document.attributes
            ):
                return False
            if (
                reply_message.gif
                or reply_message.video
                or reply_message.audio
                or reply_message.voice
            ):
                return False
            data = reply_message.media.document
        else:
            return False
    else:
        return False

    if not data or data is None:
        return False
    else:
        return data


async def remppic(delpfp):
    """ For .delpfp command, delete your current profile picture in Telegram. """
    group = delpfp.text[8:]
    if group == "all":
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1

    pfplist = await delpfp.client(
        GetUserPhotosRequest(user_id=delpfp.sender_id, offset=0, max_id=0, limit=lim)
    )
    input_photos = []
    for sep in pfplist.photos:
        input_photos.append(
            InputPhoto(
                id=sep.id,
                access_hash=sep.access_hash,
                file_reference=sep.file_reference,
            )
        )
    await delpfp.client(DeletePhotosRequest(id=input_photos))
    await delpfp.edit(f"`Successfully deleted {len(input_photos)} profile picture(s).`")


async def jon(event):
    if event.fwd_from:
        return
    mentions = "`━━━━━┓ \n┓┓┓┓┓┃\n┓┓┓┓┓┃　ヽ○ノ ⇦ Me When You Joined \n┓┓┓┓┓┃.     /　 \n┓┓┓┓┓┃ ノ) \n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃`"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(
        chat, filter=ChannelParticipantsAdmins
    ):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


async def pay(event):
    if event.fwd_from:
        return
    mentions = "`█▀▀▀▀▀█░▀▀░░░█░░░░█▀▀▀▀▀█\n█░███░█░█▄░█▀▀░▄▄░█░███░█\n█░▀▀▀░█░▀█▀▀▄▀█▀▀░█░▀▀▀░█\n▀▀▀▀▀▀▀░▀▄▀▄▀▄█▄▀░▀▀▀▀▀▀▀\n█▀█▀▄▄▀░█▄░░░▀▀░▄█░▄▀█▀░▀\n░█▄▀░▄▀▀░░░▄▄▄█░▀▄▄▄▀▄▄▀▄\n░░▀█░▀▀▀▀▀▄█░▄░████ ██▀█▄\n▄▀█░░▄▀█▀█▀░█▄▀░▀█▄██▀░█▄\n░░▀▀▀░▀░█▄▀▀▄▄░▄█▀▀▀█░█▀▀\n█▀▀▀▀▀█░░██▀█░░▄█░▀░█▄░██\n█░███░█░▄▀█▀██▄▄▀▀█▀█▄░▄▄\n█░▀▀▀░█░█░░▀▀▀░█░▀▀▀▀▄█▀░\n▀▀▀▀▀▀▀░▀▀░░▀░▀░░░▀▀░▀▀▀▀`"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(
        chat, filter=ChannelParticipantsAdmins
    ):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


async def dict(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    input_url = "https://bots.shrimadhavuk.me/dictionary/?s={}".format(input_str)
    headers = {"USER-AGENT": "PikaBot"}
    caption_str = f"Meaning of __{input_str}__\n"
    try:
        response = requests.get(input_url, headers=headers).json()
        pronounciation = response.get("p")
        meaning_dict = response.get("lwo")
        for current_meaning in meaning_dict:
            current_meaning_type = current_meaning.get("type")
            current_meaning_definition = current_meaning.get("definition")
            caption_str += (
                f"**{current_meaning_type}**: {current_meaning_definition}\n\n"
            )
    except Exception as e:
        caption_str = str(e)
    reply_msg_id = event.message.id
    if event.reply_to_msg_id:
        reply_msg_id = event.reply_to_msg_id
    try:
        await event.client.send_file(
            event.chat_id,
            pronounciation,
            caption=f"Pronounciation of __{input_str}__",
            force_document=False,
            reply_to=reply_msg_id,
            allow_cache=True,
            voice_note=True,
            silent=True,
            supports_streaming=True,
        )
    except BaseException:
        pass
    await event.edit(caption_str)


async def _ding(event):
    if event.fwd_from:
        return
    animation_interval = 0.5
    animation_ttl = range(0, 10)
    await event.edit("dong")
    animation_chars = [
        "🔴⬛⬛⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬛⬜⬜⬜\n🔴⬜⬜⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬜⬛⬜⬜\n⬜⬜🔴⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬜⬜⬛⬜\n⬜⬜⬜⬜🔴",
        "⬜⬜⬛⬛🔴\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬜⬜⬛⬜\n⬜⬜⬜⬜🔴",
        "⬜⬜⬛⬜⬜\n⬜⬜⬛⬜⬜\n⬜⬜🔴⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬛⬜⬜⬜\n🔴⬜⬜⬜⬜",
        "🔴⬛⬛⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
        "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n⬜[I Am Here mdafuk'in Bitch](t.me/PikachuUserbot) ⬜\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜",
    ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 10])


async def dlg(request):
    """ direct links generator """
    await request.edit("`Processing...`")
    textx = await request.get_reply_message()
    message = request.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await request.edit("`Usage: .direct <url>`")
        return
    reply = ""
    links = re.findall(r"\bhttps?://.*\.\S+", message)
    if not links:
        reply = "`No links found!`"
        await request.edit(reply)
    for link in links:
        if "drive.google.com" in link:
            reply += gdrive(link)
        elif "zippyshare.com" in link:
            reply += zippy_share(link)
        elif "yadi.sk" in link:
            reply += yandex_disk(link)
        elif "cloud.mail.ru" in link:
            reply += cm_ru(link)
        elif "mediafire.com" in link:
            reply += mediafire(link)
        elif "sourceforge.net" in link:
            reply += sourceforge(link)
        elif "osdn.net" in link:
            reply += osdn(link)
        elif "androidfilehost.com" in link:
            reply += androidfilehost(link)
        else:
            reply += re.findall(r"\bhttps?://(.*?[^/]+)", link)[0] + "is not supported"
    await request.edit(reply)


async def _dns(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/dns/{}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("DNS records of {} are \n{}".format(input_str, response_api))
    else:
        await event.edit("i can't seem to find {} on the internet".format(input_str))


async def urlx(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url={}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("Generated {} for {}.".format(response_api, input_str))
    else:
        await event.edit("something is wrong. please try again later.")


async def unshort(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith("3"):
        await event.edit(
            "Input URL: {}\nReDirected URL: {}".format(input_str, r.headers["Location"])
        )
    else:
        await event.edit(
            "Input URL {} returned status_code {}".format(input_str, r.status_code)
        )


async def ducgo(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://duckduckgo.com/?q={}".format(input_str.replace(" ", "+"))
    if sample_url:
        link = sample_url.rstrip()
        await event.edit(
            "Let me 🦆 DuckDuckGo that for you:\n🔎 [{}]({})".format(input_str, link)
        )
    else:
        await event.edit("something is wrong. please try again later.")


async def dump(message):
    try:
        obj = message.pattern_match.group(1)
        if len(obj) != 3:
            raise IndexError
        inp = " ".join(obj)
    except IndexError:
        inp = "🥞 🎂 🍫"
    u, t, g, o, s, n = inp.split(), "🗑", "<(^_^ <)", "(> ^_^)>", "⠀ ", "\n"
    h = [(u[0], u[1], u[2]), (u[0], u[1], ""), (u[0], "", "")]
    for something in reversed(
        [
            y
            for y in (
                [
                    "".join(x)
                    for x in (
                        f + (s, g, s + s * f.count(""), t),
                        f + (g, s * 2 + s * f.count(""), t),
                        f[:i] + (o, f[i], s * 2 + s * f.count(""), t),
                        f[:i] + (s + s * f.count(""), o, f[i], s, t),
                        f[:i] + (s * 2 + s * f.count(""), o, f[i], t),
                        f[:i] + (s * 3 + s * f.count(""), o, t),
                        f[:i] + (s * 3 + s * f.count(""), g, t),
                    )
                ]
                for i, f in enumerate(reversed(h))
            )
        ]
    ):
        for something_else in something:
            await asyncio.sleep(0.3)
            try:
                await message.edit(something_else)
            except errors.MessageIdInvalidError:
                return


async def _eval(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    cmd = event.text.split(" ", maxsplit=1)[1]
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "**EVAL**: `{}` \n\n **OUTPUT**: \n`{}` \n".format(cmd, evaluation)

    if len(final_output) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id,
            )
            await event.delete()
    else:
        await event.edit(final_output)


async def aexec(code, event):
    exec(f"async def __aexec(event): " + "".join(f"\n {l}" for l in code.split("\n")))
    return await locals()["__aexec"](event)


async def helper(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@"):
        tgbotusername = Var.TG_BOT_USER_NAME_BF_HER
        event.pattern_match.group(1)
        if tgbotusername:
            help_string = f"""Pïkå¢hµ Úsêrßð† {helpstr}"""
            results = await event.client.inline_query(  # pylint:disable=E0602
                tgbotusername, help_string
            )
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()
        else:
            await event.edit("**ERROR:** Set Var TG_BOT_USER_NAME_BF_HER")


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
            await event.edit("Pika Pi! Restarting wait for 1 Min!")
            pika_start()
            await event.delete()
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
            ax = os.environ.get("ALIVE_NAME")
            iq = await event.client.get_me()
            if iq.id == pika_id1:
                inm = ax[0]
                reply_pop_up_alert = "Hi {}'s bot here ,\n\nWhy r u clicking this this.Please get your own PikaBot, and don't use mine!".format(
                    inm
                )
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


def paginate_help(page_number, loaded_plugins, prefix):

    number_of_rows = pikrws
    number_of_cols = pikcl
    helpable_plugins = []
    for p in loaded_plugins:
        if not p.startswith("_"):
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
    elif number_of_cols == 3:
        pairs = list(
            zip(
                modules[::number_of_cols],
                modules[1::number_of_cols],
                modules[2::number_of_cols],
            )
        )
    elif number_of_cols == 4:
        pairs = list(
            zip(
                modules[::number_of_cols],
                modules[1::number_of_cols],
                modules[2::number_of_cols],
                modules[3::number_of_cols],
            )
        )
    else:
        pairs = list(
            zip(
                modules[::number_of_cols],
                modules[1::number_of_cols],
                modules[2::number_of_cols],
                modules[3::number_of_cols],
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
            + [(custom.Button.inline("⚔️Tools", data="tools"),)]
        )

    return pairs


async def _currency(event):
    if event.fwd_from:
        return
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    input_sgra = input_str.split(" ")
    if len(input_sgra) == 3:
        try:
            number = float(input_sgra[0])
            currency_from = input_sgra[1].upper()
            currency_to = input_sgra[2].upper()
            request_url = "https://api.exchangeratesapi.io/latest?base={}".format(
                currency_from
            )
            current_response = requests.get(request_url).json()
            if currency_to in current_response["rates"]:
                current_rate = float(current_response["rates"][currency_to])
                rebmun = round(number * current_rate, 2)
                await event.edit(
                    "{} {} = {} {}".format(number, currency_from, rebmun, currency_to)
                )
            else:
                await event.edit("IDEKNOWTDWTT")
        except e:
            await event.edit(str(e))
    else:
        await event.edit("`.currency number from to`")
    end = datetime.now()
    (end - start).seconds


async def _figlet(event):
    if event.fwd_from:
        return
    CMD_FIG = {
        "slant": "slant",
        "3D": "3-d",
        "5line": "5lineoblique",
        "alpha": "alphabet",
        "banner": "banner3-D",
        "doh": "doh",
        "iso": "isometric1",
        "letter": "letters",
        "allig": "alligator",
        "dotm": "dotmatrix",
        "bubble": "bubble",
        "bulb": "bulbhead",
        "digi": "digital",
    }
    input_str = event.pattern_match.group(1)
    if "|" in input_str:
        text, cmd = input_str.split("|", maxsplit=1)
    elif input_str is not None:
        cmd = None
        text = input_str
    else:
        await event.edit("Please add some text to figlet")
        return
    if cmd is not None:
        try:
            font = CMD_FIG[cmd]
        except KeyError:
            await event.edit("Invalid selected font.")
            return
        result = pyfiglet.figlet_format(text, font=font)
    else:
        result = pyfiglet.figlet_format(text)
    await event.respond("‌‌‎`{}`".format(result))
    await event.delete()


async def _getfilext(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    sample_url = "https://www.fileext.com/file-extension/{}.html"
    input_str = event.pattern_match.group(1).lower()
    response_api = requests.get(sample_url.format(input_str))
    status_code = response_api.status_code
    if status_code == 200:
        raw_html = response_api.content
        soup = BeautifulSoup(raw_html, "html.parser")
        ext_details = soup.find_all("td", {"colspan": "3"})[-1].text
        await event.edit(
            "**File Extension**: `{}`\n**Description**: `{}`".format(
                input_str, ext_details
            )
        )
    else:
        await event.edit(
            "https://www.fileext.com/ responded with {} for query: {}".format(
                status_code, input_str
            )
        )


async def _fleave(event):
    if event.fwd_from:

        return

    animation_interval = 1

    animation_ttl = range(0, 17)

    # input_str = event.pattern_match.group(1)

    # if input_str == "fleave":

    await event.edit("fleave")

    animation_chars = [
        "⬛⬛⬛\n⬛⬛⬛\n⬛⬛⬛",
        "⬛⬛⬛\n⬛🔄⬛\n⬛⬛⬛",
        "⬛⬆️⬛\n⬛🔄⬛\n⬛⬛⬛",
        "⬛⬆️↗️\n⬛🔄⬛\n⬛⬛⬛",
        "⬛⬆️↗️\n⬛🔄➡️\n⬛⬛⬛",
        "⬛⬆️↗️\n⬛🔄➡️\n⬛⬛↘️",
        "⬛⬆️↗️\n⬛🔄➡️\n⬛⬇️↘️",
        "⬛⬆️↗️\n⬛🔄➡️\n↙️⬇️↘️",
        "⬛⬆️↗️\n⬅️🔄➡️\n↙️⬇️↘️",
        "↖️⬆️↗️\n⬅️🔄➡️\n↙️⬇️↘️",
        "**Chat Message Exported To** `./Inpu/`",
        "**Chat Message Exported To** `./Inpu/homework/`",
        "**Chat Message Exported To** `./Inpu/homework/groupchat.txt`",
        "__Legend is leaving this chat.....! ",
        "__Legend is leaving this chat.....!",
    ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 17])


async def _ftext(event):
    input_str = event.pattern_match.group(1)
    if input_str:
        paytext = input_str
        pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
            paytext * 8,
            paytext * 8,
            paytext * 2,
            paytext * 2,
            paytext * 2,
            paytext * 6,
            paytext * 6,
            paytext * 2,
            paytext * 2,
            paytext * 2,
            paytext * 2,
            paytext * 2,
        )
    else:
        pay = "╭━━━╮\n┃╭━━╯\n┃╰━━╮\n┃╭━━╯\n┃┃\n╰╯\n"
    # pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(paytext*8, paytext*8, paytext*2, paytext*2, paytext*2, paytext*6, paytext*6, paytext*2, paytext*2, paytext*2, paytext*2, paytext*2)
    await event.edit(pay)


async def _fuck(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 101)
    input_str = event.pattern_match.group(1)
    if input_str == "fuck":
        await event.edit("fuck")
        animation_chars = ["👉       ✊️", "👉     ✊️", "👉  ✊️", "👉✊️💦"]
        for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 4])

    if input_str == "kiss":
        await event.edit("kiss")
        animation_chars = ["🤵       👰", "🤵     👰", "🤵  👰", "🤵💋👰"]
        for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 4])

    if input_str == "sux":
        await event.edit("sux")
        animation_chars = ["🤵       👰", "🤵     👰", "🤵  👰", "🤵👼👰"]
        for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 4])


async def _fwd(event):
    if event.fwd_from:
        return
    if Config.BOTLOG_CHATID is None:
        await event.edit(
            "Please set the required environment variable `BOTLOG_CHATID` for this plugin to work"
        )
    else:
        re_message = await event.get_reply_message()
        # https://t.me/telethonofftopic/78166
        fwd_message = await event.client.forward_messages(e, re_message, silent=True)
        await event.client.forward_messages(event.chat_id, fwd_message)
        await fwd_message.delete()
        await event.delete()


async def _gbot(event):
    if event.fwd_from:
        return
    mentions = "**🤖Bots in this Chat**: \n"
    input_str = event.pattern_match.group(1)
    to_write_chat = await event.get_input_chat()
    chat = None
    if not input_str:
        chat = to_write_chat
    else:
        mentions = "🤖Bots in {} : \n".format(input_str)
        try:
            chat = await event.client.get_entity(input_str)
        except Exception as e:
            await event.edit(str(e))
            return None
    try:
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsBots
        ):
            if isinstance(x.participant, ChannelParticipantAdmin):
                mentions += "\n 🔥 [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
            else:
                mentions += "\n [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
    except Exception as e:
        mentions += " " + str(e) + "\n"
    await event.edit(mentions)


async def _gadmins(event):
    if event.fwd_from:
        return
    mentions = "**Admins in this Channel**: \n"
    should_mention_admins = False
    reply_message = None
    pattern_match_str = event.pattern_match.group(1)
    if "m" in pattern_match_str:
        should_mention_admins = True
        if event.reply_to_msg_id:
            reply_message = await event.get_reply_message()
    input_str = event.pattern_match.group(2)
    to_write_chat = await event.get_input_chat()
    chat = None
    if not input_str:
        chat = to_write_chat
    else:
        mentions_heading = "Admins in {} channel: \n".format(input_str)
        mentions = mentions_heading
        try:
            chat = await event.client.get_entity(input_str)
        except Exception as e:
            await event.edit(str(e))
            return None
    try:
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsAdmins
        ):
            if not x.deleted:
                if isinstance(x.participant, ChannelParticipantCreator):
                    mentions += "\n 🔱 [{}](tg://user?id={}) `{}`".format(
                        x.first_name, x.id, x.id
                    )
        mentions += "\n"
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsAdmins
        ):
            if not x.deleted:
                if isinstance(x.participant, ChannelParticipantAdmin):
                    mentions += "\n 🥇 [{}](tg://user?id={}) `{}`".format(
                        x.first_name, x.id, x.id
                    )
            else:
                mentions += "\n `{}`".format(x.id)
    except Exception as e:
        mentions += " " + str(e) + "\n"
    if should_mention_admins:
        if reply_message:
            await reply_message.reply(mentions)
        else:
            await event.reply(mentions)
        await event.delete()
    else:
        await event.edit(mentions)


async def _getid(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await event.edit(
                "Current Chat ID: `{}`\nFrom User ID: `{}`\nBot API File ID: `{}`".format(
                    str(event.chat_id), str(r_msg.sender_id), bot_api_file_id
                )
            )
        else:
            await event.edit(
                "Current Chat ID: `{}`\nFrom User ID: `{}`".format(
                    str(event.chat_id), str(r_msg.sender_id)
                )
            )
    else:
        await event.edit("Current Chat ID: `{}`".format(str(event.chat_id)))
