import json
from typing import Text

from ws4py.async_websocket import WebSocket
from ws4py.messaging import TextMessage

from fancy_me.constant import (STATUS_FAILED, STATUS_OK)
from fancy_me.middleware import middle_ware
from fancy_me.context import locale


def reply(level=STATUS_OK, msg=""):
    return {"level": level, "msg": msg}


def register_user(user: Text, websocket):
    if user in locale.keys():
        return
    locale[user] = websocket


def unregister(user):
    if user not in locale.keys():
        return
    del locale[user]


class WSServer(WebSocket):

    def received_message(self, message: TextMessage) -> None:
        message = str(message.data, encoding="utf-8")
        if ">" not in message or message.count(">") > 1:
            self.send(reply(STATUS_FAILED, "请发送标准格式数据"))
            return
        mimo = message.split(">")
        event_type = mimo[0]
        try:
            effective_data = json.loads(mimo[1])
        except Exception as e:
            self.send(reply(STATUS_FAILED, "发送数据无法解析"))
            return
        user = effective_data.get("user")
        register_user(user=user, websocket=self)
        d = {'io': self, 'data': effective_data}
        middle_ware(event_type=event_type, data=d)


def send(user, message: str) -> None:
    try:
        io = locale.get(user, None)
        if isinstance(io, WSServer):
            io.send(message)
    except AttributeError:
        pass


def broadcast(message: str) -> None:
    for io in locale.values():
        io.send(message)
