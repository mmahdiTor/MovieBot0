from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from force_sub import check_force_sub


@Client.on_callback_query(filters.regex("^check_join$"))
async def check_join(client, callback):

    db = client.db
    user = callback.from_user

    is_subscribed = await check_force_sub(client, user.id)

    if not is_subscribed:
        return await callback.answer(
            "❌ هنوز عضو کانال‌ها نیستی",
            show_alert=True
        )

    try:
        await callback.message.delete()
    except:
        pass

    start_param = db.get_start_param(user.id)

    if start_param:

        db.clear_start_param(user.id)

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🎬 دریافت فیلم",
                        url=f"https://t.me/upcuckoldh_bot?start={start_param}"
                    )
                ]
            ]
        )

        await callback.message.reply_text(
            "👇 برای دریافت فیلم روی دکمه زیر کلیک کنید.",
            reply_markup=keyboard
        )

        return await callback.answer("✅ عضویت تایید شد")

    await callback.message.reply_text(
        f"👋 خوش اومدی {user.mention}"
    )

    await callback.answer("✅ عضویت تایید شد")