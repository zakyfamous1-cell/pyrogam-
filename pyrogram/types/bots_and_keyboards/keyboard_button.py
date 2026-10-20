#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from pyrogram import raw, types, utils
from ..object import Object


class KeyboardButton(Object):
    """One button of the reply keyboard.
    For simple text buttons String can be used instead of this object to specify text of the button.
    Optional fields are mutually exclusive.

    Parameters:
        text (``str``):
            Text of the button. If none of the optional fields are used, it will be sent as a message when
            the button is pressed.

        request_contact (``bool``, *optional*):
            If True, the user's phone number will be sent as a contact when the button is pressed.
            Available in private chats only.

        request_location (``bool``, *optional*):
            If True, the user's current location will be sent when the button is pressed.
            Available in private chats only.

        web_app (:obj:`~pyrogram.types.WebAppInfo`, *optional*):
            If specified, the described `Web App <https://core.telegram.org/bots/webapps>`_ will be launched when the
            button is pressed. The Web App will be able to send a “web_app_data” service message. Available in private
            chats only.

        style (:obj:`~pyrogram.enums.ButtonStyle`, *optional*):
            Color style of the button (primary, success or danger).

        icon_custom_emoji_id (``int``, *optional*):
            Unique identifier of the custom emoji shown before the text of the button.

    """

    def __init__(
        self,
        text: str,
        request_contact: bool = None,
        request_location: bool = None,
        web_app: "types.WebAppInfo" = None,
        style: "enums.ButtonStyle" = None,
        icon_custom_emoji_id: int = None
    ):
        super().__init__()

        self.text = str(text)
        self.request_contact = request_contact
        self.request_location = request_location
        self.web_app = web_app
        self.style = style
        self.icon_custom_emoji_id = icon_custom_emoji_id

    @staticmethod
    def read(b):
        t = getattr(b, "type", None)

        if isinstance(t, raw.types.ButtonTypeRequestPhone):
            return KeyboardButton(
                text=b.text,
                request_contact=True
            )

        if isinstance(t, raw.types.ButtonTypeRequestGeoLocation):
            return KeyboardButton(
                text=b.text,
                request_location=True
            )

        if isinstance(t, raw.types.ButtonTypeSimpleWebView):
            return KeyboardButton(
                text=b.text,
                web_app=types.WebAppInfo(
                    url=t.url
                )
            )

        if isinstance(b, raw.types.KeyboardButton):
            return b.text

    def write(self):
        style = utils.make_button_style(self.style, self.icon_custom_emoji_id)

        if self.request_contact:
            t = raw.types.ButtonTypeRequestPhone()
        elif self.request_location:
            t = raw.types.ButtonTypeRequestGeoLocation()
        elif self.web_app:
            t = raw.types.ButtonTypeSimpleWebView(url=self.web_app.url)
        else:
            t = raw.types.ButtonTypeDefault()

        return raw.types.KeyboardButton(text=self.text, type=t, style=style)
