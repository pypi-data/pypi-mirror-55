from ws4py.server.tulipserver import WebSocketProtocol
from fancy_me.ws.ws import register_user, WSServer, unregister, send, broadcast

__all__ = (register_user, unregister, send, broadcast)

WebSocketServer = lambda: WebSocketProtocol(WSServer)
