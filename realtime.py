import json

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornadio

tornado.websocket.WebSocketHandler.allow_draft76 = (lambda self: True)

clients = set()
current_status = 'stopped'

def broadcast(msg):
	for c in clients:
		c.send(msg)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		global current_status
		action = self.get_argument('action', None)
		if action == 'add':
			broadcast({'type': 'addMiles',
			           'miles': float(self.get_argument('miles')),
			           'monies': float(self.get_argument('monies')),
			           'anim': int(self.get_argument('anim')),
			         })
		else:
			current_status = self.get_argument('status')
			print "status:", current_status
			broadcast(current_status)
		self.write("Hello, world")


class SocketHandler(tornadio.SocketConnection):
	def on_open(self, *args, **kwargs):
		print "OPEN"
		clients.add(self)

	def on_message(self, message):
		print "MSG", message

	def on_close(self):
		print "CLOSE"
		try:
			clients.remove(self)
		except: pass

application = tornado.web.Application([
	(r'/update', MainHandler),
	tornadio.get_router(SocketHandler).route(),
])

if __name__ == '__main__':
	application.listen(5679)
	tornado.ioloop.IOLoop.instance().start()
