import json

class JSONParser(object):
	def get(self, data):
		return json.loads(data)

	def respond(self, **data):
		return json.dumps(data)