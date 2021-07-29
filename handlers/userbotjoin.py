import asyncio
from callsmusic.callsmusic import client as USER
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from helpers.decorators import errors, authorized_users_only
from helpers.filters import command
from config import SUDO_USERS, BOT_USERNAME


@Client.on_message(command(["userbotjoin", f"userbotjoin@{BOT_USERNAME}"]) & filters.group)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>make me as admin first, you can't use me if im not admin.</b>",
        )
        return
    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"
    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "i'm joined here to play music.")
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>{user.first_name} already in your chat.</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑 \n{user.first_name} can't join to this group, maybe my assistant has been banned from this group."
            f"\n\nor add @{user.username} manually to your group.</b>",
        )
        return
    await message.reply_text(
        f"<b>{user.first_name} successfully joined to your group.</b>",
    )

    
@USER.on_message(command("userbotleave") & filters.group)
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:  
        await message.reply_text(
            f"<b>assistant can't leave from group because waiting for floodwaits."
            "\n\nor kick the assistant manually.</b>",
        )
        return


@Client.on_message(command("userbotleaveall") & filters.user(SUDO_USERS) & ~filters.edited)
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        lol = await message.reply("assistant leaving all chats")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"Assistant leaving... Left: {left} chats. Failed: {failed} chats.")
            except:
                failed=failed+1
                await lol.edit(f"Assistant leaving... Left: {left} chats. Failed: {failed} chats.")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"Left {left} chats. Failed {failed} chats.")
