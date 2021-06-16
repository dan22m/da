import loguru
from aiogram import Bot, Dispatcher, executor, types, asyncio
from aiogram.types import InputFile, User
from config import *
from answer import dev_cmd_button_link,dev_cmd_text_btn,dev_cmd_text_msg,start_cmd_msg_text,user_left_msg_text,help_cmd_msg_text,bots_cmd_msg_text, rules_cmd_msg_text, AniLinks
from loguru import logger
import logging
import os
import shutil
import platform
import psutil
import tracemalloc
from time import sleep
import shlex
from subprocess import Popen, PIPE, STDOUT
import subprocess
import sqlite3



logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

logger.add("log_file.log", format="{time}  {level}  {message}",
level="DEBUG")


conn = sqlite3.connect('rules.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS rulesdb(
   chat_id INT PRIMARY KEY,
   rules TEXT);
""")
conn.commit()


async def on_startup(dispatcher: Dispatcher):
    await bot.send_message(Daniel_Maklein_ID,f"Bot Start!")
    await set_default_commands(dispatcher)
    logger.info(f"Bot Succesfully started")


async def set_default_commands(dp):
    logger.info('Установка комманд бота...')
    await dp.bot.set_my_commands([
        types.BotCommand("dev", "Розробник"),
        types.BotCommand("help", "help"),
        types.BotCommand("stat", "к-сть msg")
#        types.BotCommand({cmd_set_2}, {cmd_set_hlp_2})
    ])


@dp.message_handler(commands="set_rules", commands_prefix='/!.',is_chat_admin=True)
async def cmd_setrules(message: types.Message):
    rules_text=str.partition(message.text,' ')[2]
    db_rules=(message.chat.id,rules_text, rules_text)
    cur.execute("INSERT INTO rulesdb (chat_id, rules) VALUES(?, ?) ON CONFLICT (chat_id) DO UPDATE SET rules = ?",db_rules)
    conn.commit()
    await message.answer(f"Параметр правил встановлено:\ntext: \n{rules_text}",disable_notification=True, disable_web_page_preview=True)
    logger.debug(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} t.me/{message.chat.username} chat_id:{message.chat.id}\n"
        f"ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /set_rules\n"
        f"\n"
        f"{rules_text}"
        f"\n---------------------------------------------------------\n"
    ) 




@dp.message_handler(commands="rules", commands_prefix='/!.')
async def cmd_rules(message: types.Message):
    try:
        chat_id=message.chat.id
        cur.execute("SELECT rules FROM rulesdb WHERE chat_id=" + str(chat_id))
        rules_send2 = cur.fetchone()[0]
        await message.answer(rules_send2)
    except: 
        await message.answer("ERROR\nправила не збережені\n використайте інструкцію\nhttps://telegra.ph/Ustanovka-pravil-dlya-chatu-06-14\nякщо все ще не зрозуміло як назначити зверніться до творця /dev")

    
    
@dp.message_handler(commands='dev',commands_prefix="!/.")
async def cmd_dev(message: types.Message):
    admin_markup = types.InlineKeyboardMarkup(row_width=3)
    admin_markup.insert(
        types.InlineKeyboardButton(
            text=dev_cmd_text_btn,
            url=dev_cmd_button_link
        )
    )
    logger.info(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"@{message.from_user.username}:{message.from_user.id}\n"
        f"use /dev"
        f"\n---------------------------------------------------------\n"
    )
    await message.answer(
        text=''.join(
            (
                dev_cmd_text_msg
            )
        ),
        reply_markup=admin_markup
    )



    
@dp.message_handler(
    commands=["logs"],
    commands_prefix="!/."
)
async def cmd_new_log(message: types.Message):
    await message.delete()
    await bot.send_document(Daniel_Maklein_ID, InputFile("log_file.log"))
    await bot.send_document(SBEDN_ID, InputFile("log_file.log"))
    logger.debug(
        f"\n--------------------------------------------------------\n"
        f"NEW BACKUP LOG CREATE AND SENT TO CREATOR"
        f"\n---------------------------------------------------------\n"
    )

#------------------------------------------/BAN /UNBAN--------------------------------------------------   , is_chat_admin=True
#--------------------------------------------------------------------------------------------------------------------------------

@dp.message_handler(
    commands=["ban"],
    commands_prefix="!/.",
    is_reply=True,
    is_chat_admin=True
)
async def cmd_ban(message: types.Message):
    try:
        await message.chat.kick(message.reply_to_message.from_user.id)
        await bot.send_message(message.chat.id,f"*{message.reply_to_message.from_user.first_name}*\nбув заблокований адміном:\n*{message.from_user.first_name}*", disable_notification=True)
        logger.debug(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /ban\n"
        f"**{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n---------------------------------------------------------\n"
    )   
    except:
        admin_markup = types.InlineKeyboardMarkup(row_width=3)
        admin_markup.insert(
        types.InlineKeyboardButton(
            text=dev_cmd_text_btn,
            url=dev_cmd_button_link
        )
    )
    await message.reply(f"cmd_ban ERROR\nзверніться до розробника\nза допомогою кнопки нижче",reply_markup=admin_markup)            
    logger.error(
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"ERROR  {message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ERROR  ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"ERROR  use /ban\n"
        f"ERROR  **{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
    )


#reason=> ***{message.reply_to_message.text}***
#


@dp.message_handler(
    commands=["unban"],
    commands_prefix="!/.",
    is_reply=True,
    is_chat_admin=True
)
async def cmd_unban(message: types.Message):
    try:
        await message.chat.unban(message.reply_to_message.from_user.id)
        logger.debug(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /unban\n"
        f"**{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n---------------------------------------------------------\n"
    )
        await bot.send_message(message.chat.id,f"*{message.reply_to_message.from_user.first_name}* \nбув розблокований адміном: \n*{message.from_user.first_name}*", disable_notification=True)
    except:
        admin_markup = types.InlineKeyboardMarkup(row_width=3)
    admin_markup.insert(
        types.InlineKeyboardButton(
            text=dev_cmd_text_btn,
            url=dev_cmd_button_link
        )
    )
    await message.reply(f"cmd_unban ERROR\nзверніться до розробника\nза допомогою кнопки нижче",reply_markup=admin_markup)            
    logger.error(
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"ERROR  {message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ERROR  ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"ERROR  use /unban\n"
        f"ERROR  **{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
    )



@dp.message_handler(
    commands=["mute"],
    commands_prefix="!/.",
    is_reply=True,
    is_chat_admin=True
)
async def cmd_mute(message: types.Message):
    try:
        await message.chat.restrict(message.reply_to_message.from_user.id, can_send_messages=False)
        logger.debug(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /mute\n"
        f"**{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n---------------------------------------------------------\n"
    )
        await bot.send_message(message.chat.id,f"*{message.reply_to_message.from_user.first_name}* \nбув приглушений адміном: \n*{message.from_user.first_name}*",disable_notification=True)
    except:
        admin_markup = types.InlineKeyboardMarkup(row_width=3)
    admin_markup.insert(
        types.InlineKeyboardButton(
            text=dev_cmd_text_btn,
            url=dev_cmd_button_link
        )
    )
    await message.reply(f"cmd_mute ERROR\nзверніться до розробника\nза допомогою кнопки нижче",reply_markup=admin_markup)            
    logger.error(
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"ERROR  {message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ERROR  ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"ERROR  use /mute\n"
        f"ERROR  **{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
    )




@dp.message_handler(
    commands=["unmute"],
    commands_prefix="!/.",
    is_reply=True,
    is_chat_admin=True
)
async def cmd_unmute(message: types.Message):
    try:
        await message.chat.restrict(message.reply_to_message.from_user.id,
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True
    )
        logger.debug(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /unmute\n"
        f"**{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n---------------------------------------------------------\n"
    )
        await bot.send_message(message.chat.id,f"*{message.reply_to_message.from_user.first_name}* \nбув розглушений адміном: \n*{message.from_user.first_name}*",disable_notification=True)
        await message.delete()
    except:
        admin_markup = types.InlineKeyboardMarkup(row_width=3)
    admin_markup.insert(
        types.InlineKeyboardButton(
            text=dev_cmd_text_btn,
            url=dev_cmd_button_link
        )
    )
    await message.reply(f"cmd_unmute ERROR\nзверніться до розробника\nза допомогою кнопки нижче",reply_markup=admin_markup)            
    logger.error(
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"ERROR  {message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ERROR  ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"ERROR  use /unmute\n"
        f"ERROR  **{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
    )




@dp.message_handler(
    commands=["kick"],
    commands_prefix="!/.",
    is_reply=True,
    is_chat_admin=True
)
async def cmd_kick(message: types.Message):
    try:
        await message.chat.unban(message.reply_to_message.from_user.id)
        logger.debug(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /kick\n"
        f"**{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n---------------------------------------------------------\n"
    )
        await bot.send_message(message.chat.id,f"*{message.reply_to_message.from_user.first_name}* \nбув вигнаний з чату адміном: \n*{message.from_user.first_name}*",disable_notification=True)
    except:
        admin_markup = types.InlineKeyboardMarkup(row_width=3)
    admin_markup.insert(
        types.InlineKeyboardButton(
            text=dev_cmd_text_btn,
            url=dev_cmd_button_link
        )
    )
    await message.reply(f"cmd_kick ERROR\nзверніться до розробника\nза допомогою кнопки нижче",reply_markup=admin_markup)            
    logger.error(
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"ERROR  {message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ERROR  ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"ERROR  use /kick\n"
        f"ERROR  **{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
    )




#______________________________________________________________________________
#______________________________________________________________________________

@dp.message_handler(
    commands=["sban"],
    commands_prefix="!/.",
    is_reply=True,
    is_chat_admin=True
)
async def cmd_sban(message: types.Message):
    try:
        await message.chat.kick(message.reply_to_message.from_user.id)
        logger.debug(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /sban\n"
        f"**{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n---------------------------------------------------------\n"
    )
    except:
        admin_markup = types.InlineKeyboardMarkup(row_width=3)
    admin_markup.insert(
        types.InlineKeyboardButton(
            text=dev_cmd_text_btn,
            url=dev_cmd_button_link
        )
    )
    await message.reply(f"cmd_sban ERROR\nзверніться до розробника\nза допомогою кнопки нижче",reply_markup=admin_markup)            
    logger.error(
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"ERROR  {message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ERROR  ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"ERROR  use /sban\n"
        f"ERROR  **{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
    )





@dp.message_handler(
    commands=["sunban"],
    commands_prefix="!/.",
    is_reply=True,
    is_chat_admin=True
)
async def cmd_sunban(message: types.Message):
    try:
        await message.delete()
        await message.chat.unban(message.reply_to_message.from_user.id)
        logger.debug(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /sunban\n"
        f"**{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n---------------------------------------------------------\n"
    )
    except:
        admin_markup = types.InlineKeyboardMarkup(row_width=3)
    admin_markup.insert(
        types.InlineKeyboardButton(
            text=dev_cmd_text_btn,
            url=dev_cmd_button_link
        )
    )
    await message.reply(f"cmd_sunban ERROR\nзверніться до розробника\nза допомогою кнопки нижче",reply_markup=admin_markup)            
    logger.error(
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"ERROR  {message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ERROR  ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"ERROR  use /sunban\n"
        f"ERROR  **{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
    )





@dp.message_handler(
    commands=["smute"],
    commands_prefix="!/.",
    is_reply=True,
    is_chat_admin=True
)
async def cmd_smute(message: types.Message):
    try:
        await message.delete()
        await message.chat.restrict(message.reply_to_message.from_user.id, can_send_messages=False)
        logger.debug(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /smute\n"
        f"**{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n---------------------------------------------------------\n"
    )
    except:
        admin_markup = types.InlineKeyboardMarkup(row_width=3)
    admin_markup.insert(
        types.InlineKeyboardButton(
            text=dev_cmd_text_btn,
            url=dev_cmd_button_link
        )
    )
    await message.reply(f"cmd_smute ERROR\nзверніться до розробника\nза допомогою кнопки нижче",reply_markup=admin_markup)            
    logger.error(
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"ERROR  {message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ERROR  ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"ERROR  use /smute\n"
        f"ERROR  **{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
    )
    





@dp.message_handler(
    commands=["sunmute"],
    commands_prefix="!/.",
    is_reply=True,
    is_chat_admin=True
)
async def cmd_sunmute(message: types.Message):
    try:
        await message.delete()
        await message.chat.restrict(message.reply_to_message.from_user.id,
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True
    )
        logger.debug(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /sunmute\n"
        f"**{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n---------------------------------------------------------\n"
    )
    except:
        admin_markup = types.InlineKeyboardMarkup(row_width=3)
    admin_markup.insert(
        types.InlineKeyboardButton(
            text=dev_cmd_text_btn,
            url=dev_cmd_button_link
        )
    )
    await message.reply(f"cmd_sunmute ERROR\nзверніться до розробника\nза допомогою кнопки нижче",reply_markup=admin_markup)            
    logger.error(
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"ERROR  {message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ERROR  ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"ERROR  use /sunmute\n"
        f"ERROR  **{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
    )


@dp.message_handler(
    commands=["skick"],
    commands_prefix="!/.",
    is_reply=True,
    is_chat_admin=True
)
async def cmd_skick(message: types.Message):
    try:
        await message.delete()
        await message.chat.unban(message.reply_to_message.from_user.id)
        logger.debug(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /skick\n"
        f"**{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n---------------------------------------------------------\n"
        )
    except:
        admin_markup = types.InlineKeyboardMarkup(row_width=3)
    admin_markup.insert(
        types.InlineKeyboardButton(
            text=dev_cmd_text_btn,
            url=dev_cmd_button_link
        )
    )
    await message.answer(f"cmd_skick ERROR\nзверніться до розробника\nза допомогою кнопки нижче",reply_markup=admin_markup)            
    logger.error(
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"ERROR  {message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"ERROR  ADMIN @{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"ERROR  use /skick\n"
        f"ERROR  **{message.reply_to_message.from_user.first_name}**  @{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
    )







#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------


@dp.message_handler(commands="id", commands_prefix='/!.')
async def cmd_id(message: types.Message):
    await message.answer(f'Чат ID = {message.chat.id}\nТип чату = {message.chat.type}', disable_notification=True)
    logger.info(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"@{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /id"
        f"\n---------------------------------------------------------\n"
    )


@dp.message_handler(content_types=["new_chat_members"])
async def new_chat_member(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, вітаю тебе в нашому чаті!")
    logger.debug(
        f"\n---------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"NEW CHAT MEMBER\n"
        f"@{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"\n---------------------------------------------------------\n"
    )

@dp.message_handler(content_types=["left_chat_member"])
async def user_left(message: types.Message):
    logger.debug(
        f"\n---------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"MEMBER LEFT\n"
        f"@{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"\n---------------------------------------------------------\n"
    )





@dp.message_handler(commands="start", commands_prefix='/!.')
async def cmd_start(message: types.Message):
    await message.answer(start_cmd_msg_text)
    logger.info(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"@{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /start"
        f"\n---------------------------------------------------------\n"
    )

@dp.message_handler(commands="help", commands_prefix='/!.')
async def cmd_help(message: types.Message):
    await message.reply(help_cmd_msg_text)
    logger.info(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"@{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /help"
        f"\n---------------------------------------------------------\n"
    )


@dp.message_handler(commands="bots",commands_prefix="/!.")
async def asdasd(message: types.Message):
    await message.answer(bots_cmd_msg_text, disable_notification=True)
    logger.info(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"@{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /bots\n"
        f"\n---------------------------------------------------------"
    )

@dp.message_handler(
    commands=["stat"],
    commands_prefix="!/."
)
async def cmd_stat(message: types.Message):
    await message.answer(f"к-сть повідомлень в чаті = {message.message_id}")
    logger.debug(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"@{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /stat\n"
        f"\n---------------------------------------------------------\n"
    )


@dp.message_handler(commands="rules", commands_prefix='/!.')
async def cmd_rules(message: types.Message):
    await message.answer(rules_cmd_msg_text)
    logger.info(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"@{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /rules"
        f"\n---------------------------------------------------------\n"
    )


cpu_usage=psutil.cpu_percent(4)
ram_usage=psutil.virtual_memory()[2]

@dp.message_handler(commands="ping", commands_prefix='/!.')
async def cmd_ping(message: types.Message):
        await message.answer(f"CPU load = {cpu_usage}% \nRAM load = {ram_usage}%")
        logger.debug(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"@{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /ping\n"
        f"####CPU load = {cpu_usage}% \nRAM load = {ram_usage}%####"
        f"\n---------------------------------------------------------\n"
    )



@dp.message_handler(commands="ua_chats", commands_prefix='/!.')
async def cmd_ua_chats(message: types.Message):
        await message.answer(AniLinks)
        logger.debug(
        f"\n--------------------------------------------------------\n"
        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
        f"@{message.from_user.username}:{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}\n"
        f"use /ua_chats\n"
        f"\n---------------------------------------------------------\n"
    )











#@dp.message_handler(commands="t", commands_prefix='/!.')
#async def cmd_test(message: types.Message):
#        await message.answer(f"CPU load = {cpu_usage}%\nRAM load = {ram_usage}% \n\n\n\n {message.reply_to_message.from_user.first_name}\n\n\n  Ім'я:{message.from_user.first_name}  Прізвище:{message.from_user.last_name}")
#        logger.debug("е")
#        print(f"ааааааааа")



#    logger.debug(
#        f"\n--------------------------------------------------------\n"
#        f"{message.chat.title} @{message.chat.username} chat_id:{message.chat.id}\n"
#        f"ADMIN @{message.from_user.username}:{message.from_user.id}\n"
#        f"use /skick\n"
#        f"@{message.reply_to_message.from_user.username}:{message.reply_to_message.from_user.id}\n"
#        f"\n---------------------------------------------------------\n"
#    )





if __name__ == '__main__':
    executor.start_polling(dp,on_startup=on_startup, skip_updates=SKIP_UPDATES)