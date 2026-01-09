# Auto Approval Bot

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, add_channel, all_users, all_groups, all_channels, users, groups, channels, remove_user, save_session, get_session, delete_session, is_logged_in
from configs import cfg
import random, asyncio

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

# Bot Image
BOT_IMAGE = "https://graph.org/file/5f86083e1abbd1bdb6788-9e43cc508d9e56391f.jpg"

# Store login states (phone_hash, client instances)
login_states = {}
user_clients = {}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m : Message):
    op = m.chat
    kk = m.from_user
    try:
        # Check if it's a channel or group and add to correct collection
        if m.chat.type == enums.ChatType.CHANNEL:
            add_channel(m.chat.id)
        else:
            add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, kk.id)
        await app.send_message(kk.id, "**Hello {}!\nWelcome To {}**".format(m.from_user.mention, m.chat.title))
        add_user(kk.id)
    except errors.PeerIdInvalid as e:
        print("user isn't start bot(means group)")
    except Exception as err:
        print(str(err))    
 
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.command("start"))
async def start_command(_, m: Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id)
    except Exception as e:
        print(f"Error in get_chat_member: {e}")
        try:
            invite_link = await app.create_chat_invite_link(cfg.CHID)
        except Exception as err:
            print(f"Error in create_chat_invite_link: {err}")
            await m.reply(f"**❌ Make Sure I Am Admin In Your Channel!**\n\n**Error:** `{err}`\n**Channel ID:** `{cfg.CHID}`")
            return 
        key = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("🍿 Join Update Channel 🍿", url=invite_link.invite_link),
                InlineKeyboardButton("🍀 Check Again 🍀", callback_data="chk")
            ]]
        ) 
        await m.reply_text("**⚠️Access Denied!⚠️\n\nPlease Join My Update Channel To Use Me. If You Joined The Channel Then Click On Check Again Button To Confirm.**", reply_markup=key)
        return 
    
    add_user(m.from_user.id)
    bot_me = await app.get_me()
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🤖 Add to Group", url=f"https://t.me/{bot_me.username}?startgroup=true"),
            InlineKeyboardButton("📢 Add to Channel", url=f"https://t.me/{bot_me.username}?startchannel=true")
        ],
        [
            InlineKeyboardButton("⚡ Bulk Approve", callback_data="bulk_approve"),
            InlineKeyboardButton("📖 Help Menu", callback_data="help_menu")
        ]
    ])
    
    caption = f"""**Best Channel Management Bot,
Top #1 on Telegram**

👋 Hey {m.from_user.mention},
➡ Accept New Join Requests
➡ Accept Pending Join Requests"""
    
    await m.reply_photo(BOT_IMAGE, caption=caption, reply_markup=keyboard)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Callbacks ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
    except Exception as e:
        print(f"Error in chk get_chat_member: {e}")
        await cb.answer("🙅‍♂️ You are not joined my channel first join channel then check again. 🙅‍♂️", show_alert=True)
        return 
    
    add_user(cb.from_user.id)
    bot_me = await app.get_me()
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🤖 Add to Group", url=f"https://t.me/{bot_me.username}?startgroup=true"),
            InlineKeyboardButton("📢 Add to Channel", url=f"https://t.me/{bot_me.username}?startchannel=true")
        ],
        [
            InlineKeyboardButton("⚡ Bulk Approve", callback_data="bulk_approve"),
            InlineKeyboardButton("📖 Help Menu", callback_data="help_menu")
        ]
    ])
    
    caption = f"""**Best Channel Management Bot,
Top #1 on Telegram**

👋 Hey {cb.from_user.mention},
➡ Accept New Join Requests
➡ Accept Pending Join Requests"""
    
    await cb.message.edit_caption(caption=caption, reply_markup=keyboard)

@app.on_callback_query(filters.regex("main_menu"))
async def main_menu_cb(_, cb: CallbackQuery):
    bot_me = await app.get_me()
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🤖 Add to Group", url=f"https://t.me/{bot_me.username}?startgroup=true"),
            InlineKeyboardButton("📢 Add to Channel", url=f"https://t.me/{bot_me.username}?startchannel=true")
        ],
        [
            InlineKeyboardButton("⚡ Bulk Approve", callback_data="bulk_approve"),
            InlineKeyboardButton("📖 Help Menu", callback_data="help_menu")
        ]
    ])
    
    caption = f"""**Best Channel Management Bot,
Top #1 on Telegram**

👋 Hey {cb.from_user.mention},
➡ Accept New Join Requests
➡ Accept Pending Join Requests"""
    
    await cb.message.edit_caption(caption=caption, reply_markup=keyboard)

@app.on_callback_query(filters.regex("help_menu"))
async def help_menu_cb(_, cb: CallbackQuery):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ])
    
    caption = """**Here Is My Help Menu**

<u>User Commands To Be Used In Groups And Pm</u>

<blockquote>» /start : Starts The Bot.
» /help : Showcase The Help Menu.
» /info [id/username/reply]: Extract Information.
» /id [username or reply]: Extract The Id.</blockquote>

<u>Miscellaneous Commands</u>

<blockquote>» /approveall : Bulk Pending Requests Approve.
» /stats : Check Bot Statistics</blockquote>"""
    
    await cb.message.edit_caption(caption=caption, reply_markup=keyboard, parse_mode=enums.ParseMode.HTML)

@app.on_callback_query(filters.regex("bulk_approve"))
async def bulk_approve_cb(_, cb: CallbackQuery):
    bot_me = await app.get_me()
    user_id = cb.from_user.id
    
    # Check if user is logged in
    logged_in = is_logged_in(user_id)
    login_status = "✅ Connected" if logged_in else "❌ Not Connected"
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔐 Login", callback_data="login"),
            InlineKeyboardButton("📤 Logout", callback_data="logout")
        ],
        [
            InlineKeyboardButton("✅ Approve All", callback_data="approve_all"),
            InlineKeyboardButton("📚 Tutorial", callback_data="tutorial")
        ],
        [
            InlineKeyboardButton("🤖 Add to Group", url=f"https://t.me/{bot_me.username}?startgroup=true"),
            InlineKeyboardButton("📢 Add to Channel", url=f"https://t.me/{bot_me.username}?startchannel=true")
        ],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ])
    
    caption = f"""**⚡ Insane Speed Bulk Approval Feature**

**Account Status:** {login_status}

◆  🔐 Login – Connect your account.
◆  📤 Logout – Disconnect your account.
◆  ✅ Approve All – Use /approve to approve requests
◆  📚 Tutorial – Tutorial to understand how this works."""
    
    await cb.message.edit_caption(caption=caption, reply_markup=keyboard)

@app.on_callback_query(filters.regex("^login$"))
async def login_cb(_, cb: CallbackQuery):
    user_id = cb.from_user.id
    
    # Check if already logged in
    if is_logged_in(user_id):
        await cb.answer("✅ You are already logged in! Use Logout first.", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Cancel", callback_data="bulk_approve")]
    ])
    
    # Set login state
    login_states[user_id] = {"step": "phone"}
    
    await cb.message.edit_caption(
        caption="""**🔐 Login to Your Account**

Please send your **phone number** with country code.

**Example:** `+919876543210`

⚠️ Your session will be securely stored and used only for approving join requests.""",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex("^logout$"))
async def logout_cb(_, cb: CallbackQuery):
    user_id = cb.from_user.id
    
    if not is_logged_in(user_id):
        await cb.answer("❌ You are not logged in!", show_alert=True)
        return
    
    # Delete session from database
    delete_session(user_id)
    
    # Disconnect client if active
    if user_id in user_clients:
        try:
            await user_clients[user_id].stop()
        except:
            pass
        del user_clients[user_id]
    
    await cb.answer("✅ Successfully logged out!", show_alert=True)
    
    # Refresh the bulk approve menu
    bot_me = await app.get_me()
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔐 Login", callback_data="login"),
            InlineKeyboardButton("📤 Logout", callback_data="logout")
        ],
        [
            InlineKeyboardButton("✅ Approve All", callback_data="approve_all"),
            InlineKeyboardButton("📚 Tutorial", callback_data="tutorial")
        ],
        [
            InlineKeyboardButton("🤖 Add to Group", url=f"https://t.me/{bot_me.username}?startgroup=true"),
            InlineKeyboardButton("📢 Add to Channel", url=f"https://t.me/{bot_me.username}?startchannel=true")
        ],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ])
    
    caption = """**⚡ Insane Speed Bulk Approval Feature**

**Account Status:** ❌ Not Connected

◆  🔐 Login – Connect your account.
◆  📤 Logout – Disconnect your account.
◆  ✅ Approve All – Use /approve to approve requests
◆  📚 Tutorial – Tutorial to understand how this works."""
    
    await cb.message.edit_caption(caption=caption, reply_markup=keyboard)

@app.on_callback_query(filters.regex("approve_all"))
async def approve_all_cb(_, cb: CallbackQuery):
    user_id = cb.from_user.id
    
    if is_logged_in(user_id):
        await cb.answer("✅ Use /approve <channel_username> command to approve all pending requests using your connected account!", show_alert=True)
    else:
        await cb.answer("❌ Please login first to use this feature!\n\nOr use /approveall in your group/channel.", show_alert=True)

@app.on_callback_query(filters.regex("tutorial"))
async def tutorial_cb(_, cb: CallbackQuery):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="bulk_approve")]
    ])
    
    caption = """**📚 Tutorial - How to Use Bulk Approve**

**Method 1: Using Bot (Slower)**
1. Add bot to your group/channel as admin
2. Use /approveall command in the chat

**Method 2: Using Your Account (Faster) ⚡**
1. Click Login and enter your phone number
2. Enter the OTP code sent to your Telegram
3. Use /approve @channel_username to approve all requests

**Why Login?**
Using your own account allows faster bulk approval without hitting bot rate limits!

⚠️ Your session is encrypted and secure."""
    
    await cb.message.edit_caption(caption=caption, reply_markup=keyboard)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Login Handler ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.text & ~filters.command(["start", "help", "info", "id", "stats", "users", "approveall", "approve", "bcast", "fcast"]))
async def handle_login_messages(_, m: Message):
    user_id = m.from_user.id
    
    if user_id not in login_states:
        return
    
    state = login_states[user_id]
    
    if state["step"] == "phone":
        phone = m.text.strip()
        
        # Validate phone number
        if not phone.startswith("+"):
            await m.reply("❌ Please include country code (e.g., +919876543210)")
            return
        
        await m.reply("📲 Sending OTP to your phone...")
        
        try:
            # Create a new client for this user
            user_client = Client(
                f"user_{user_id}",
                api_id=cfg.API_ID,
                api_hash=cfg.API_HASH,
                in_memory=True
            )
            
            await user_client.connect()
            
            # Send code
            sent_code = await user_client.send_code(phone)
            
            login_states[user_id] = {
                "step": "otp",
                "phone": phone,
                "phone_code_hash": sent_code.phone_code_hash,
                "client": user_client
            }
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Cancel", callback_data="cancel_login")]
            ])
            
            await m.reply(
                "**✅ OTP Sent!**\n\nPlease enter the **OTP code** you received.\n\n**Format:** `1 2 3 4 5` (with spaces)\n\n⚠️ This is to prevent Telegram from detecting it as a code.",
                reply_markup=keyboard
            )
            
        except Exception as e:
            await m.reply(f"❌ Error: {str(e)}\n\nPlease try again.")
            if user_id in login_states:
                del login_states[user_id]
    
    elif state["step"] == "otp":
        otp = m.text.replace(" ", "").strip()
        
        try:
            user_client = state["client"]
            phone = state["phone"]
            phone_code_hash = state["phone_code_hash"]
            
            # Sign in
            try:
                await user_client.sign_in(phone, phone_code_hash, otp)
            except errors.SessionPasswordNeeded:
                login_states[user_id]["step"] = "2fa"
                await m.reply("**🔒 2FA Enabled**\n\nPlease enter your **2FA password**:")
                return
            
            # Get session string
            session_string = await user_client.export_session_string()
            
            # Save to database
            save_session(user_id, session_string, phone)
            
            # Store client
            user_clients[user_id] = user_client
            
            # Clean up
            del login_states[user_id]
            
            await m.reply("**✅ Successfully Logged In!**\n\nYou can now use /approve @channel_username to bulk approve join requests using your account.\n\nUse the Logout button to disconnect.")
            
        except Exception as e:
            await m.reply(f"❌ Error: {str(e)}\n\nPlease try again from Login.")
            if user_id in login_states:
                try:
                    await state["client"].disconnect()
                except:
                    pass
                del login_states[user_id]
    
    elif state["step"] == "2fa":
        password = m.text.strip()
        
        try:
            user_client = state["client"]
            phone = state["phone"]
            
            # Check password
            await user_client.check_password(password)
            
            # Get session string
            session_string = await user_client.export_session_string()
            
            # Save to database
            save_session(user_id, session_string, phone)
            
            # Store client
            user_clients[user_id] = user_client
            
            # Clean up
            del login_states[user_id]
            
            await m.reply("**✅ Successfully Logged In!**\n\nYou can now use /approve @channel_username to bulk approve join requests using your account.")
            
        except Exception as e:
            await m.reply(f"❌ Wrong password or error: {str(e)}\n\nPlease try again.")

@app.on_callback_query(filters.regex("cancel_login"))
async def cancel_login_cb(_, cb: CallbackQuery):
    user_id = cb.from_user.id
    
    if user_id in login_states:
        try:
            if "client" in login_states[user_id]:
                await login_states[user_id]["client"].disconnect()
        except:
            pass
        del login_states[user_id]
    
    await cb.answer("❌ Login cancelled!", show_alert=True)
    
    # Go back to bulk approve menu
    bot_me = await app.get_me()
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔐 Login", callback_data="login"),
            InlineKeyboardButton("📤 Logout", callback_data="logout")
        ],
        [
            InlineKeyboardButton("✅ Approve All", callback_data="approve_all"),
            InlineKeyboardButton("📚 Tutorial", callback_data="tutorial")
        ],
        [
            InlineKeyboardButton("🤖 Add to Group", url=f"https://t.me/{bot_me.username}?startgroup=true"),
            InlineKeyboardButton("📢 Add to Channel", url=f"https://t.me/{bot_me.username}?startchannel=true")
        ],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ])
    
    caption = """**⚡ Insane Speed Bulk Approval Feature**

**Account Status:** ❌ Not Connected

◆  🔐 Login – Connect your account.
◆  📤 Logout – Disconnect your account.
◆  ✅ Approve All – Use /approve to approve requests
◆  📚 Tutorial – Tutorial to understand how this works."""
    
    await cb.message.edit_caption(caption=caption, reply_markup=keyboard)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Approve Command ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.command("approve"))
async def approve_command(_, m: Message):
    user_id = m.from_user.id
    
    if not is_logged_in(user_id):
        await m.reply("❌ You need to login first!\n\nUse the **Bulk Approve** menu to login.")
        return
    
    if len(m.command) < 2:
        await m.reply("**Usage:** /approve @channel_username or /approve -100xxxx")
        return
    
    chat_input = m.command[1]
    
    lel = await m.reply("**⚡ Connecting to your account...**")
    
    try:
        # Get or create user client
        if user_id in user_clients:
            user_client = user_clients[user_id]
            if not user_client.is_connected:
                await user_client.connect()
        else:
            session_data = get_session(user_id)
            if not session_data:
                await lel.edit("❌ Session not found. Please login again.")
                return
            
            user_client = Client(
                f"user_{user_id}",
                api_id=cfg.API_ID,
                api_hash=cfg.API_HASH,
                session_string=session_data["session_string"]
            )
            await user_client.connect()
            user_clients[user_id] = user_client
        
        await lel.edit("**⚡ Fetching pending join requests...**")
        
        # Get chat
        try:
            if chat_input.startswith("-100"):
                chat = await user_client.get_chat(int(chat_input))
            else:
                chat = await user_client.get_chat(chat_input)
        except Exception as e:
            await lel.edit(f"❌ Could not find chat: {e}")
            return
        
        await lel.edit(f"**⚡ Approving requests in {chat.title}...**")
        
        approved = 0
        failed = 0
        
        try:
            async for request in user_client.get_chat_join_requests(chat.id):
                try:
                    await user_client.approve_chat_join_request(chat.id, request.user.id)
                    approved += 1
                    
                    if approved % 10 == 0:
                        await lel.edit(f"**⚡ Approved {approved} users...**")
                        
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    try:
                        await user_client.approve_chat_join_request(chat.id, request.user.id)
                        approved += 1
                    except:
                        failed += 1
                except:
                    failed += 1
        except Exception as e:
            await lel.edit(f"❌ Error: {e}")
            return
        
        await lel.edit(f"""**✅ Bulk Approval Complete!**

📊 **Chat:** {chat.title}
✅ **Approved:** `{approved}`
❌ **Failed:** `{failed}`""")
        
    except Exception as e:
        await lel.edit(f"❌ Error: {str(e)}\n\nTry logging in again.")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Help Command ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("help"))
async def help_command(_, m: Message):
    help_text = """**📖 Help Menu**

<u>User Commands To Be Used In Groups And Pm</u>

<blockquote>» /start : Starts The Bot.
» /help : Showcase The Help Menu.
» /info [id/username/reply]: Extract Information.
» /id [username or reply]: Extract The Id.</blockquote>

<u>Miscellaneous Commands</u>

<blockquote>» /approveall : Bulk Pending Requests Approve.
» /approve @channel : Approve using your account.
» /stats : Check Bot Statistics</blockquote>"""
    
    await m.reply_text(help_text, parse_mode=enums.ParseMode.HTML)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Info Command ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("info"))
async def info_command(_, m: Message):
    user = None
    
    if m.reply_to_message:
        user = m.reply_to_message.from_user
    elif len(m.command) > 1:
        try:
            user_input = m.command[1]
            if user_input.isdigit():
                user = await app.get_users(int(user_input))
            else:
                user = await app.get_users(user_input)
        except Exception as e:
            await m.reply_text(f"**❌ Error:** Could not find user.\n`{e}`")
            return
    else:
        user = m.from_user
    
    info_text = f"""**👤 User Information**

**🆔 ID:** `{user.id}`
**👤 First Name:** {user.first_name}
**📛 Last Name:** {user.last_name or 'None'}
**🔗 Username:** @{user.username or 'None'}
**🤖 Is Bot:** {user.is_bot}
**📱 DC ID:** {user.dc_id or 'Unknown'}"""
    
    await m.reply_text(info_text)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ID Command ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("id"))
async def id_command(_, m: Message):
    user_id = None
    
    if m.reply_to_message:
        user_id = m.reply_to_message.from_user.id
        username = m.reply_to_message.from_user.username or "None"
    elif len(m.command) > 1:
        try:
            user_input = m.command[1]
            if user_input.startswith("@"):
                user_input = user_input[1:]
            user = await app.get_users(user_input)
            user_id = user.id
            username = user.username or "None"
        except Exception as e:
            await m.reply_text(f"**❌ Error:** Could not find user.\n`{e}`")
            return
    else:
        user_id = m.from_user.id
        username = m.from_user.username or "None"
    
    await m.reply_text(f"**🆔 User ID:** `{user_id}`\n**🔗 Username:** @{username}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Stats Command ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command(["users", "stats"]))
async def stats_command(_, m: Message):
    xx = all_users()
    x = all_groups()
    c = all_channels()
    tot = int(xx + x + c)
    
    if m.from_user.id in cfg.SUDO:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📄 Send Log File", callback_data="send_log_file")]
        ])
        await m.reply_text(text=f"""
🍀 **Bot Statistics** 🍀

🙋‍♂️ **Users:** `{xx}`
👥 **Groups:** `{x}`
📢 **Channels:** `{c}`
🚧 **Total:** `{tot}`""", reply_markup=keyboard)
    else:
        await m.reply_text(text=f"""
🍀 **Bot Statistics** 🍀

🚧 **Total Users & Groups:** `{tot}`""")

@app.on_callback_query(filters.regex("send_log_file"))
async def send_log_file_cb(_, cb: CallbackQuery):
    user_id = cb.from_user.id
    
    # Check if user is admin
    if user_id not in cfg.SUDO:
        await cb.answer("❌ Only admins can access this!", show_alert=True)
        return
    
    await cb.answer("📄 Generating log file...")
    
    try:
        # Get all users, groups and channels from database
        all_users_list = list(users.find({}))
        all_groups_list = list(groups.find({}))
        all_channels_list = list(channels.find({}))
        
        log_content = "═══════════════════════════════════\n"
        log_content += "          BOT LOG FILE\n"
        log_content += "═══════════════════════════════════\n\n"
        
        log_content += f"📊 Total Users: {len(all_users_list)}\n"
        log_content += f"📊 Total Groups: {len(all_groups_list)}\n"
        log_content += f"📊 Total Channels: {len(all_channels_list)}\n\n"
        
        log_content += "═══════════════════════════════════\n"
        log_content += "              USERS\n"
        log_content += "═══════════════════════════════════\n\n"
        
        for idx, usr in enumerate(all_users_list, 1):
            user_id_db = usr.get("user_id", "Unknown")
            try:
                user_info = await app.get_users(int(user_id_db))
                username = f"@{user_info.username}" if user_info.username else "No Username"
                name = user_info.first_name or "Unknown"
                log_content += f"{idx}. {name} | {username} | ID: {user_id_db}\n"
            except:
                log_content += f"{idx}. Unknown User | ID: {user_id_db}\n"
        
        log_content += "\n═══════════════════════════════════\n"
        log_content += "             GROUPS\n"
        log_content += "═══════════════════════════════════\n\n"
        
        for idx, grp in enumerate(all_groups_list, 1):
            chat_id_db = grp.get("chat_id", "Unknown")
            try:
                chat_info = await app.get_chat(int(chat_id_db))
                chat_title = chat_info.title or "Unknown"
                chat_username = f"@{chat_info.username}" if chat_info.username else "No Username"
                log_content += f"{idx}. {chat_title} | {chat_username} | ID: {chat_id_db}\n"
            except:
                log_content += f"{idx}. Unknown Group | ID: {chat_id_db}\n"
        
        log_content += "\n═══════════════════════════════════\n"
        log_content += "            CHANNELS\n"
        log_content += "═══════════════════════════════════\n\n"
        
        for idx, chnl in enumerate(all_channels_list, 1):
            chat_id_db = chnl.get("chat_id", "Unknown")
            try:
                chat_info = await app.get_chat(int(chat_id_db))
                chat_title = chat_info.title or "Unknown"
                chat_username = f"@{chat_info.username}" if chat_info.username else "No Username"
                log_content += f"{idx}. {chat_title} | {chat_username} | ID: {chat_id_db}\n"
            except:
                log_content += f"{idx}. Unknown Channel | ID: {chat_id_db}\n"
        
        log_content += "\n═══════════════════════════════════\n"
        log_content += "          END OF LOG FILE\n"
        log_content += "═══════════════════════════════════"
        
        # Save to file
        import os
        log_file_path = "bot_log.txt"
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write(log_content)
        
        # Send file
        await cb.message.reply_document(
            document=log_file_path,
            caption="📄 **Bot Log File**\n\nContains all users, groups, and channels information."
        )
        
        # Delete the file after sending
        os.remove(log_file_path)
        
    except Exception as e:
        await cb.message.reply(f"❌ Error generating log file: {e}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Approve All Command ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("approveall") & (filters.group | filters.channel))
async def approveall_command(_, m: Message):
    # Check if user is admin
    try:
        member = await app.get_chat_member(m.chat.id, m.from_user.id)
        if member.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
            await m.reply_text("**❌ Only admins can use this command!**")
            return
    except Exception as e:
        await m.reply_text(f"**❌ Error:** `{e}`")
        return
    
    # Check if bot is admin
    try:
        bot_member = await app.get_chat_member(m.chat.id, (await app.get_me()).id)
        if bot_member.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
            await m.reply_text("**❌ I need to be an admin with 'Add Members' permission!**")
            return
    except Exception as e:
        await m.reply_text(f"**❌ Error:** `{e}`")
        return
    
    lel = await m.reply_text("**⚡ Approving all pending join requests...**")
    
    approved = 0
    failed = 0
    
    try:
        async for request in app.get_chat_join_requests(m.chat.id):
            try:
                await app.approve_chat_join_request(m.chat.id, request.user.id)
                approved += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await app.approve_chat_join_request(m.chat.id, request.user.id)
                    approved += 1
                except:
                    failed += 1
            except Exception as e:
                failed += 1
    except Exception as e:
        await lel.edit(f"**❌ Error fetching requests:** `{e}`")
        return
    
    await lel.edit(f"""**✅ Bulk Approval Complete!**

✅ **Approved:** `{approved}`
❌ **Failed:** `{failed}`""")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅ Successful to `{success}` users.\n❌ Failed to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅ Successful to `{success}` users.\n❌ Failed to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

print("I'm Alive Now!")
app.run()
