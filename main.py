from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory
import json
import threading
import time
from GameManager import Game
from PlayerAI import PlayerAI

class MyServerProtocol(WebSocketServerProtocol):

    def __init__(self):
        self.g = Game()
        self.g.setPlayerAI(PlayerAI())
        self.g.updateGrid = self.UpdateGameStatus
        self.commands = {
            "StartNewGame": threading.Thread(target=self.g.Start).start
        }
    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        try:
            obj = json.loads(payload.decode('utf8'))
            msg = obj['msg']
            if(not self.commands.__contains__(msg)):
                raise Exception('Command not found (\'' + msg + '\')')
            
            reply = self.commands[msg]()

            self.sendMessage(json.dumps({
                "reply": msg,
                "data": reply
            }).encode('UTF-8'))

        except Exception as ex:
            self.sendMessage(json.dumps(
                {
                    'error': str(ex)
                }).encode('UTF-8'))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    def UpdateGameStatus(self, grid):
        self.sendMessage(json.dumps(
            {
                'push': 'status_update',
                'data': grid.map
            }).encode('UTF-8'))

def stop_loop():
    input('press any key...')
    loop.call_soon_threadsafe(loop.stop)

if __name__ == '__main__':
    import asyncio

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    server = loop.run_until_complete(coro)
    
    threading.Thread(target=stop_loop).start()
    # input('server started')
    loop.run_forever()
    loop.close()