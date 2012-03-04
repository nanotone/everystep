import urllib2

import pymongo
from bson.objectid import ObjectId

import flask
app = flask.Flask(__name__)

db = pymongo.Connection().everystep

@app.route('/')
def index():
	return "hello"

@app.route('/user/<uid>')
def user(uid):
	uid = ObjectId(uid)
	return str(db.users.find_one({'_id': uid}))

@app.route('/status/<running>')
def status(running):
	print "RUNNING", running
	urllib2.urlopen('http://localhost:5679/update?status=%s' % running).read()
	return running

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5678, debug=True)
