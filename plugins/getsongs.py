""" Songs Module
{i}getsong song name
"""
# created by @mrconfused

import glob
import os

from selenium import webdriver
from userbot import ALIVE_NAME

DEFAULTUSER = ALIVE_NAME


@ItzSjDude(pattern="getsong( (.*)|$)")
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    repl = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif repl:
        if repl.message:
            query = repl.message
    else:
        await event.reply("`What I am Supposed to find `")
        return
    a = await event.reply("`wi8..! I am finding your song....`")
    await catmusic(str(query), "320k", event)
    l = glob.glob("./temp/*.mp3")
    if l:
        await a.edit("yeah..! i found something wi8..🥰")
    else:
        await a.edit(f"Sorry..! i can't find anything with `{query}`")
        return
    thumbcat = glob.glob("./temp/*.jpg") + glob.glob("./temp/*.webp")
    if thumbcat:
        catthumb = thumbcat[0]
    else:
        catthumb = None
    loa = l[0]
    await event.client.send_file(
        event.chat_id,
        loa,
        force_document=False,
        allow_cache=False,
        caption=f"➥ __**Song :- {query}**__\n__**➥ Uploaded by :-**__ {DEFAULTUSER}",
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await a.delete()
    os.system("rm -rf ./temp/*.mp3")
    os.system("rm -rf ./temp/*.jpg")
    os.system("rm -rf ./temp/*.webp")


async def catmusic(cat, QUALITY, hello):
    search = cat
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = Var.CHROME_BIN
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.youtube.com/results?search_query=" + search)
    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for i in user_data:
        video_link = i.get_attribute("href")
        break
    if not os.path.isdir("./temp/"):
        os.makedirs("./temp/")
    if not video_link:
        await hello.reply(f"Sorry. I can't find that song `{search}`")
        return
    try:
        command = (
            'youtube-dl -o "./temp/%(title)s.%(ext)s" --extract-audio --audio-format mp3 --audio-quality '
            + QUALITY
            + " "
            + video_link
        )
        os.system(command)
    except Exception as e:
        return await hello.reply(f"`Error:\n {e}`")
    try:
        thumb = (
            'youtube-dl -o "./temp/%(title)s.%(ext)s" --write-thumbnail --skip-download '
            + video_link
        )
        os.system(thumb)
    except Exception as e:
        return await hello.reply(f"`Error:\n {e}`")
