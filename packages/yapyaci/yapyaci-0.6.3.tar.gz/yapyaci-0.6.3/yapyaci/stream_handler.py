from .object_set import AciSet, AciTree, ListOfAciTree, to_tree, mpprint
from abc import ABC, abstractmethod
import threading
import websocket
import logging
import ssl
import json

logger1 = logging.getLogger(__name__)

class StreamHandler(ABC, threading.Thread):
    def __init__(self, ctx, *args, **kwargs):
        super(StreamHandler, self).__init__(*args, **kwargs)
        self._stream = None
        self._ctx=ctx

    def run(self):
        ws_opt = {
            "cert_reqs": ssl.CERT_NONE,
            "check_hostname": False
        }

        logger1.error('Starting websocket with url {0}'.format(self._ctx.ws_url))

        #websocket.enableTrace(True)
        self._stream = websocket.WebSocketApp(self._ctx.ws_url, header=self._ctx.http_header, on_message=self._handler, on_error=self._on_error, on_close=self._on_close, on_open=self._on_open)
        self._stream.run_forever(sslopt=ws_opt)

    def _on_error(self, error):
        logger1.critical(error)
        self._ctx.ws_status = "ERROR"

    def _on_close(self):
        logger1.warning('WebSocket has been closed')
        self._ctx.ws_status = "CLOSE"

    def _on_open(self):
        logger1.warning('WebSocket has been opened')
        self._ctx.ws_status = "OPEN"

    def kill_thread(self):
        logger1.warning("Closing the WebSocket...")
        self._stream.close()

    @abstractmethod
    def _handler(self, message):
        pass

class PrintStream(StreamHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _handler(self, msg):
        logger1.debug('Websocket has received a message')
        obj = AciTree(json.loads(msg))

        mpprint(obj)




