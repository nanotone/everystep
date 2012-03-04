import json

import tornado.ioloop
import tornado.web
import tornado.websocket

tornado.websocket.WebSocketHandler.allow_draft76 = (lambda self: True)

clients = []
current_status = 'stopped'

def broadcast(msg):
	msg = json.dumps(msg)
	for c in clients:
		c.write_message(msg)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		global current_status
		if self.get_argument('action') == 'add':
			broadcast({'type': 'addMiles',
			           'miles': float(self.get_argument('miles')),
			           'monies': float(self.get_argument('monies')),
			         })
		else:
			current_status = self.get_argument('status')
			print "status arg:", current_status
			broadcast(current_status)
		self.write("Hello, world")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print "OPEN"
		#self.write_message(current_status)
		clients.append(self)

	def on_message(self, message):
		print "MSG", message

	def on_close(self):
		print "CLOSE"
		clients.remove(self)

application = tornado.web.Application([
	(r'/', MainHandler),
	(r'/websocket', WebSocketHandler),
])

if __name__ == '__main__':
	application.listen(5679)
	tornado.ioloop.IOLoop.instance().start()
