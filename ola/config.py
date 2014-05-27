from subscriber.ajax import SubscriberAjaxHandler

class RestApiMap(object):
	@staticmethod
	def get(handle):
		handles = {
			'subscriber' : SubscriberAjaxHandler
		}
		return handles[handle]