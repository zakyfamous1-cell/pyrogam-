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

from datetime import datetime
from typing import Union

import pyrogram
from pyrogram import raw, types, utils


class SendRichMessage:
    async def send_rich_message(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        rich_message: "types.InputRichMessage",
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        message_thread_id: int = None,
        partial_reply: str = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        message_effect_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "types.Message":
        """Send a rich message (tables, in-message buttons, ...).

        Rich messages can only be sent by bot accounts.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            rich_message (:obj:`~pyrogram.types.InputRichMessage`):
                The rich message to send.

            disable_notification (``bool``, *optional*):
                Sends the message silently.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum.

            partial_reply (``str``, *optional*):
                Quote text for a partial reply.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            message_effect_id (``int``, *optional*):
                Unique identifier of the message effect (private chats only).

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | ..., *optional*):
                Additional interface options.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent message is returned.

        Example:
            .. code-block:: python

                from pyrogram.types import InputRichMessage

                await app.send_rich_message(
                    chat_id,
                    InputRichMessage(html="<h3>Order</h3><table><tr><th>Item</th><th>Qty</th></tr>"
                                          "<tr><td>Tea</td><td>2</td></tr></table>"))
        """
        reply_to = utils.get_reply_head_fm(message_thread_id, reply_to_message_id, partial_reply)

        r = await self.invoke(
            raw.functions.messages.SendMessage(
                peer=await self.resolve_peer(chat_id),
                silent=disable_notification or None,
                reply_to=reply_to,
                random_id=self.rnd_id(),
                schedule_date=utils.datetime_to_timestamp(schedule_date),
                reply_markup=await reply_markup.write(self) if reply_markup else None,
                message="",
                rich_message=await rich_message.write(self),
                effect=int(message_effect_id) if message_effect_id else None,
                noforwards=protect_content
            )
        )

        if isinstance(r, raw.types.UpdateShortSentMessage):
            from pyrogram import enums

            peer = await self.resolve_peer(chat_id)

            peer_id = (
                peer.user_id
                if isinstance(peer, raw.types.InputPeerUser)
                else -peer.chat_id
            )

            return types.Message(
                id=r.id,
                chat=types.Chat(id=peer_id, type=enums.ChatType.PRIVATE, client=self),
                date=utils.timestamp_to_datetime(r.date),
                outgoing=r.out,
                reply_markup=reply_markup,
                client=self
            )

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateNewMessage,
                              raw.types.UpdateNewChannelMessage,
                              raw.types.UpdateNewScheduledMessage)):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage)
                )
