import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from app.config import BOT_TOKEN, APP_URL, BACKUP_CHANNEL_URL, MAIN_CHANNEL_ID, ADMIN_IDS
from app.db import init_db, upsert_user, add_post, latest_message_id, user_count

bot = Bot(8656736053:AAET1pZpa9lbfNGe_SFFbiSAw-L1riUUZ54)
dp = Dispatcher()

def main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Open Channel", web_app=WebAppInfo(url=APP_URL))],
        [InlineKeyboardButton(text="📢 Backup Channel", url=BACKUP_CHANNEL_URL)]
    ])

@dp.message(CommandStart())
async def start(message: Message):
    u = message.from_user
    upsert_user(u.id, u.username, u.first_name)
    await message.answer(
        "🔥 <b>Welcome!</b> ✅\n\n"
        "👇 Post dekhne ke liye <b>Open Channel</b> par click karo 😉♦️",
        reply_markup=main_keyboard(),
        parse_mode="HTML"
    )

@dp.message(Command("stats"))
async def stats(message: Message):
    if ADMIN_IDS and message.from_user.id not in ADMIN_IDS:
        return
    await message.answer(f"👥 Users: {user_count()}")

@dp.channel_post()
async def channel_post(message: Message):
    # Add the bot as an administrator to your main channel first.
    if MAIN_CHANNEL_ID and str(message.chat.id) != str(MAIN_CHANNEL_ID):
        return

    text = message.text or ""
    caption = message.caption or ""
    media_type, file_id = "", ""

    if message.photo:
        media_type, file_id = "photo", message.photo[-1].file_id
    elif message.video:
        media_type, file_id = "video", message.video.file_id
    elif message.animation:
        media_type, file_id = "animation", message.animation.file_id
    elif message.document:
        media_type, file_id = "document", message.document.file_id

    before = latest_message_id(message.chat.id)
    add_post(message.chat.id, message.message_id, text, media_type, file_id, caption)
    after = latest_message_id(message.chat.id)

    # Notify users about the new post. For the first run, this sends a 1-post notice.
    # If you don't want user notifications, remove the broadcast block below.
    from app.db import conn
    with conn() as c:
        users = [r["user_id"] for r in c.execute("SELECT user_id FROM users").fetchall()]

    if users:
        msg = (
            "🔥 <b>1 New Post Uploaded!</b> ✅\n\n"
            "👇 <b>Tap below to view</b>"
        )
        for uid in users:
            try:
                await bot.send_message(uid, msg, reply_markup=main_keyboard(), parse_mode="HTML")
            except Exception:
                pass

async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=["message", "channel_post"])

if __name__ == "__main__":
    asyncio.run(main())
