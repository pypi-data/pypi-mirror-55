import json
from asyncio import DatagramProtocol, transports, DatagramTransport
from typing import Optional
from fancy_me.middleware import middle_ware


class DataServer(DatagramProtocol):
    def data_received(self, data: bytes) -> None:
        d = str(data, encoding='utf-8')
        if ">" not in d or d.count(">") > 1:
            return
        mimo = d.split(">")
        event_type = mimo[0]
        try:
            effective_data = json.loads(mimo[1])
        except Exception as e:
            print(e)
            return
        middle_ware(event_type=event_type, data=effective_data)

    def error_received(self, exc: Exception) -> None:
        pass

    def connection_lost(self, exc: Optional[Exception]) -> None:
        pass

    def connection_made(self, transport: transports.BaseTransport) -> None:
        pass

    def eof_received(self):
        pass
