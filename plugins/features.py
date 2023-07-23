import re, asyncio, os, sys
import time
import random
from pyrogram import Client, filters, enums
from pyrogram.types import *
from info import ADMINS
from time import time, sleep
from plugins.helper_functions.admin_check import admin_check
from Script import script
from plugins.helper_functions.extract import extract_time, extract_user
from plugins.helper_functions.cust_p_filters import f_onw_fliter
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, UserAdminInvalid
import Speedtest

speedtester = Speedtest.Speedtest()
def get_ping():
    speedtester.get_best_server()
    ping = speedtester.results.ping
    return ping
ALIVE = "<b>ʜɪ ɪ ᴀᴍ ᴀʟɪɴᴇ ʙʀᴜʜ🥵</b>"


#_______RESTART______   
@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def stop_button(bot, message):
    msg = await bot.send_message(text="**🔄 𝙿𝚁𝙾𝙲𝙴𝚂𝚂𝙴𝚂 𝚂𝚃𝙾𝙿𝙴𝙳. 𝙱𝙾𝚃 𝙸𝚂 𝚁𝙴𝚂𝚃𝙰𝚁𝚃𝙸𝙽𝙶...**", chat_id=message.chat.id)       
    await asyncio.sleep(3)
    await msg.edit("**✅️ 𝙱𝙾𝚃 𝙸𝚂 𝚁𝙴𝚂𝚃𝙰𝚁𝚃𝙴𝙳. 𝙽𝙾𝚆 𝚈𝙾𝚄 𝙲𝙰𝙽 𝚄𝚂𝙴 𝙼𝙴**")
    os.execl(sys.executable, sys.executable, *sys.argv)

#________PURGE______

@Client.on_message(filters.command("purge") & (filters.group | filters.channel))                   
async def purge(client, message):
    if message.chat.type not in ((enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL)):
        return
    is_admin = await admin_check(message)
    if not is_admin:
        return

    status_message = await message.reply_text("...", quote=True)
    await message.delete()
    message_ids = []
    count_del_etion_s = 0

    if message.reply_to_message:
        for a_s_message_id in range(message.reply_to_message.id, message.id):
            message_ids.append(a_s_message_id)
            if len(message_ids) == "100":
                await client.delete_messages(
                    chat_id=message.chat.id,
                    message_ids=message_ids,
                    revoke=True
                )
                count_del_etion_s += len(message_ids)
                message_ids = []
        if len(message_ids) > 0:
            await client.delete_messages(
                chat_id=message.chat.id,
                message_ids=message_ids,
                revoke=True
            )
            count_del_etion_s += len(message_ids)
    await status_message.edit_text(f"deleted {count_del_etion_s} messages")
    await asyncio.sleep(5)
    await status_message.delete()
    
#ban
@Client.on_message(filters.command("ban"))
async def ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return 
    user_id, user_first_name = extract_user(message)
    try:
        await message.chat.ban_member(user_id=user_id)
    except Exception as error:
        await message.reply_text(str(error))                    
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(f"Someone else is dusting off..! \n{user_first_name} \nIs forbidden.")                              
        else:
            await message.reply_text(f"Someone else is dusting off..! \n<a href='tg://user?id={user_id}'>{user_first_name}</a> Is forbidden")                      

@Client.on_message(filters.command(["unban", "unmute"]))
async def un_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    user_id, user_first_name = extract_user(message)
    try:
        await message.chat.unban_member(user_id=user_id)
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "Okay, changed ... now "
                f"{user_first_name} To "
                " You can join the group!"
            )
        else:
            await message.reply_text(
                "Okay, changed ... now "
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a> To "
                " You can join the group!"
            )
            
@Client.on_message(filters.command("tban"))
async def temp_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    if not len(message.command) > 1:
        return
    user_id, user_first_name = extract_user(message)
    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        return await message.reply_text(text=f"Invalid time type specified. \nExpected m, h, or d, Got it: {message.command[1][-1]}")   
    try:
        await message.chat.ban_member(user_id=user_id, until_date=until_date_val)            
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(f"Someone else is dusting off..!\n{user_first_name}\nbanned for {message.command[1]}!")
        else:
            await message.reply_text(f"Someone else is dusting off..!\n<a href='tg://user?id={user_id}'>Lavane</a>\n banned for {message.command[1]}!")
                

#report

@Client.on_message((filters.command(["report"]) | filters.regex("@admins") | filters.regex("@admin")) & filters.group)
async def report_user(bot, message):
    if message.reply_to_message:
        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention
        success = True
        report = f"𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})" + "\n"
        report += f"𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {message.reply_to_message.link}"
        # Using latest pyrogram's enums to filter out chat administrators
        async for admin in bot.get_chat_members(chat_id=message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if not admin.user.is_bot: # Filtering bots and prevent sending message to bots | Message will be send only to user admins
                try:
                    reported_post = await message.reply_to_message.forward(admin.user.id)
                    await reported_post.reply_text(
                        text=report,
                        chat_id=admin.user.id,
                        disable_web_page_preview=True
                    )
                    success = True
                except:
                    pass
            else: # Skipping Bots
                pass
        if success:
            await message.reply_text(script.REPRT_MSG)
          
#ping and alive command
@Client.on_message(filters.command("alive", "/") & f_onw_fliter)
async def check_alive(_, message):
    await message.reply_text(ALIVE)


@Client.on_message(filters.command("ping", prefixes='/') & filters.private)
async def ping_command(_, message):
    start_t = time.time()
    rm = await message.reply_text("Pinging...")
    ping = get_ping()
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"📶Ping📶: {ping} ms\n🚩Response time🚩: {time_taken_s:.3f} ms")

#_______________

@Client.on_message(filters.group & filters.command('inkick'))
def inkick(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
    if len(message.command) > 1:
      input_str = message.command
      sent_message = message.reply_text(script.START_KICK)
      sleep(20)
      sent_message.delete()
      message.delete()
      count = 0
      for member in client.get_chat_members(message.chat.id):
        if member.user.status in input_str and not member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
          try:
            client.ban_chat_member(message.chat.id, member.user.id, int(time() + 45))
            count += 1
            sleep(1)
          except (ChatAdminRequired, UserAdminInvalid):
            sent_message.edit(script.ADMIN_REQUIRED)
            client.leave_chat(message.chat.id)
            break
          except FloodWait as e:
            sleep(e.x)
      try:
        sent_message.edit(script.KICKED.format(count))
      except ChatWriteForbidden:
        pass
    else:
      message.reply_text(script.INPUT_REQUIRED)
  else:
    sent_message = message.reply_text(script.CREATOR_REQUIRED)
    sleep(5)
    sent_message.delete()
    message.delete()


@Client.on_message(filters.group & filters.command('dkick'))
def dkick(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
    sent_message = message.reply_text(script.START_KICK)
    sleep(20)
    sent_message.delete()
    message.delete()
    count = 0
    for member in client.get_chat_members(message.chat.id):
      if member.user.is_deleted and not member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        try:
          client.ban_chat_member(message.chat.id, member.user.id, int(time() + 45))
          count += 1
          sleep(1)
        except (ChatAdminRequired, UserAdminInvalid):
          sent_message.edit(script.ADMIN_REQUIRED)
          client.leave_chat(message.chat.id)
          break
        except FloodWait as e:
          sleep(e.x)
    try:
      sent_message.edit(script.DKICK.format(count))
    except ChatWriteForbidden:
      pass
  else:
    sent_message = message.reply_text(script.CREATOR_REQUIRED)
    sleep(5)
    sent_message.delete()
    message.delete()

  
@Client.on_message((filters.channel | filters.group) & filters.command('instatus'))
def instatus(client, message):
    sent_message = message.reply_text("🔁 Processing.....")
    recently = 0
    within_week = 0
    within_month = 0
    long_time_ago = 0
    deleted_acc = 0
    uncached = 0
    bot = 0
    for member in client.get_chat_members(message.chat.id, limit=int(10000)):
      user = member.user
      if user.is_deleted:
        deleted_acc += 1
      elif user.is_bot:
        bot += 1
      elif user.status == enums.UserStatus.RECENTLY:
        recently += 1
      elif user.status == enums.UserStatus.LAST_WEEK:
        within_week += 1
      elif user.status == enums.UserStatus.LAST_MONTH:
        within_month += 1
      elif user.status == enums.UserStatus.LONG_AGO:
        long_time_ago += 1
      else:
        uncached += 1

    chat_type = message.chat.type
    if chat_type == enums.ChatType.CHANNEL:
         sent_message.edit(f"{message.chat.title}\nChat Member Status\n\nRecently - {recently}\nWithin Week - {within_week}\nWithin Month - {within_month}\nLong Time Ago - {long_time_ago}\n\nDeleted Account - {deleted_acc}\nBot - {bot}\nUnCached - {uncached}")            
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        user = client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER, ADMINS):
            sent_message.edit(f"{message.chat.title}\nChat Member Status\n\nRecently - {recently}\nWithin Week - {within_week}\nWithin Month - {within_month}\nLong Time Ago - {long_time_ago}\n\nDeleted Account - {deleted_acc}\nBot - {bot}\nUnCached - {uncached}")
        else:
            sent_message.edit("you are not administrator in this chat")


  
