# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/URL-Shortner-Bot/blob/main/LICENSE

import os
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from pyshorteners import Shortener

CUTTLY_API = os.environ.get("CUTTLY_API", None)

BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text='⚙ Join X Channel ⚙', url='https://telegram.me/JAVSTORE_robot')
        ]]
    )

@Client.on_message(filters.private & filters.regex(r'https?://[^\s]+'))
async def reply_shortens(bot, update):
    message = await update.reply_text(
        text="`Analysing your link...`",
        disable_web_page_preview=True,
        quote=True
    )
    link = update.matches[0].group(0)
    shorten_urls = await short(link)
    await message.edit_text(
        text=shorten_urls,
        reply_markup=BUTTONS,
        disable_web_page_preview=True
    )

@Client.on_inline_query(filters.regex(r'https?://[^\s]+'))
async def inline_short(bot, update):
    link = update.matches[0].group(0)
    shorten_urls = await short(link)
    answers = [
        InlineQueryResultArticle(
            title="Short Links",
            description=update.query,
            input_message_content=InputTextMessageContent(
                message_text=shorten_urls,
                disable_web_page_preview=True
            ),
            reply_markup=BUTTONS
        )
    ]
    await bot.answer_inline_query(
        inline_query_id=update.id,
        results=answers
    )

async def short(link):
    shorten_urls = "**--Shorted URLs--**\n"
    
    if CUTTLY_API:
        try:
            s = Shortener(api_key=CUTTLY_API)
            url = s.cuttly.short(link)
            shorten_urls += f"\n**Cutt.ly :-** {url}"
        except Exception as error:
            print(f"Cutt.ly error :- {error}")
    
    # Send the text
    try:
        shorten_urls += "\n\nMade by AssFucker!"
        return shorten_urls
    except Exception as error:
        return error
