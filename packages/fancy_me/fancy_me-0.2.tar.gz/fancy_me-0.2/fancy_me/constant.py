STATUS_OK  = "ok"
STATUS_FAILED = "wrong"
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
    set_name(self, user)
    d = {'io': self, 'data': effective_data}

