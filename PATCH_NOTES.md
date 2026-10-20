# Patch: message effects, button styles, custom emoji on buttons

Schema source: Telegram Desktop api.tl (layer 231). Only additive, write-only constructors were
added to compiler/api/source/main_api.tl. The declared layer stays 166, so incoming updates
keep parsing exactly like before.

Rebuild the raw API after copying this folder (needed once):

    cd compiler/api && python compiler.py
    cd ../errors && python compiler.py
    (or: pip install .   -> setup.py does it)

## Usage

    from pyrogram import enums
    from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    await client.send_message(
        chat_id, '<emoji id="5368324170671202286">🔥</emoji> halo',
        parse_mode=enums.ParseMode.HTML,
        message_effect_id=5104841245755180586,          # private chats only
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Hijau", callback_data="ok",
                                 style=enums.ButtonStyle.SUCCESS,
                                 icon_custom_emoji_id=5368324170671202286),
            InlineKeyboardButton("Merah", url="https://t.me", style=enums.ButtonStyle.DANGER),
        ]]))

    await message.reply_text("hi", message_effect_id=5104841245755180586)

- style: ButtonStyle.PRIMARY (blue) / SUCCESS (green) / DANGER (red) / DEFAULT
- Also available on KeyboardButton (reply keyboard).
- message_effect_id works on send_message/photo/video/document/audio/voice/animation/sticker/
  video_note/cached_media/contact/location/venue/poll/dice/media_group and Message.reply_*.
- If any button in an inline keyboard has style/icon, the whole keyboard is sent in the new format.
- Custom emoji in text already worked: <emoji id="...">x</emoji> with ParseMode.HTML.

Not included: reading effect_id / style back from incoming messages (needs a full layer bump).

## Rich message (table + in-message pill buttons)

Added `types.InputRichMessage`, `types.InputRichMessageMedia`, `Client.send_rich_message(...)` and
`edit_message_text(..., rich_message=...)` (text is now optional). The HTML is parsed by Telegram, so
`<table>`, `<h3>`, `<tg-button-row><tg-button style="success" ...>` and `<tg-emoji>` work.
Same API names as kurigram, so helpers written for kurigram (e.g. botvvip1/modules/ui.py) run unchanged.

    from pyrogram.types import InputRichMessage
    await app.send_rich_message(chat_id, InputRichMessage(
        html='<h3>Order</h3><table><tr><th>Item</th><th>Qty</th></tr><tr><td>Tea</td><td>2</td></tr></table>'
             '<tg-button-row><tg-button type="callback_data" style="danger" data="cancel">Batal</tg-button></tg-button-row>'))

- Rich messages only work from BOT accounts (not userbots).
- Media inside a rich message supports file_id only. URLs/paths raise, and ui.py then sends the media separately.
- Reading rich messages back from incoming updates is not implemented.
