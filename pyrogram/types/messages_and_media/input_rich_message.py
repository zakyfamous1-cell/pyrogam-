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

from typing import List, Optional

import pyrogram
from pyrogram import raw, utils
from ..object import Object


class InputRichMessageMedia(Object):
    """A photo or video embedded inside a rich message.

    Reference it in the HTML with ``<img src="tg://photo?id=KEY"/>`` or
    ``<video src="tg://video?id=KEY"></video>``.

    Parameters:
        id (``str``):
            Key used to reference the media from the HTML.

        media (:obj:`~pyrogram.types.InputMediaPhoto` | :obj:`~pyrogram.types.InputMediaVideo`):
            The media. Only file_id strings are supported.
    """

    def __init__(self, id: str, media):
        super().__init__()

        self.id = id
        self.media = media

    def write(self):
        source = getattr(self.media, "media", self.media)

        if not isinstance(source, str):
            raise ValueError("InputRichMessageMedia only supports file_id strings")

        m = utils.get_input_media_from_file_id(source)

        if isinstance(m, raw.types.InputMediaPhoto):
            return raw.types.InputRichFilePhoto(id=self.id, photo=m.id)

        return raw.types.InputRichFileDocument(id=self.id, document=m.id)


class InputRichMessage(Object):
    """A rich message (tables, headings, in-message buttons, ...) written in Telegram rich HTML.

    The HTML is parsed by Telegram itself, so tags such as ``<table>``, ``<h3>``, ``<tg-button-row>``,
    ``<tg-button>`` and ``<tg-emoji>`` are supported. Rich messages can only be sent by bot accounts.

    Parameters:
        html (``str``):
            Rich HTML content.

        media (List of :obj:`~pyrogram.types.InputRichMessageMedia`, *optional*):
            Media files referenced from the HTML.

        rtl (``bool``, *optional*):
            Right-to-left layout.

        noautolink (``bool``, *optional*):
            Disable automatic link detection.
    """

    def __init__(
        self,
        html: str,
        media: Optional[List["InputRichMessageMedia"]] = None,
        rtl: bool = None,
        noautolink: bool = None
    ):
        super().__init__()

        self.html = html
        self.media = media
        self.rtl = rtl
        self.noautolink = noautolink

    async def write(self, client: "pyrogram.Client"):
        return raw.types.InputRichMessageHTML(
            html=self.html,
            rtl=self.rtl or None,
            noautolink=self.noautolink or None,
            files=[m.write() for m in self.media] if self.media else None
        )
