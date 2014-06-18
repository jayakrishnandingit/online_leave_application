import re
import threading
from django.core.mail import send_mail
from constants import LEAVE_REQUEST_SUBJECT, LEAVE_REQUEST_MSG, EMAIL_REGEX
from ola.settings import DATETIME_INPUT_FORMATS

class SendNotification(threading.Thread):
	def __init__(self, to_addr, from_addr, callback, *args):
		threading.Thread.__init__(self)

		self.to_addr = self._clean_to_addr(to_addr)
		self.from_addr = self._clean_from_addr(from_addr)
		self.callback = callback
		self.args = args

	def _clean_to_addr(self, addr):
		if not addr:
			raise Exception('No to addresses')
		if not isinstance(addr, list):
			try:
				addr = [addr]
			except:
				raise Exception('Must be of type or convertible to list')
		for each in addr:
			if not re.match(EMAIL_REGEX, each):
				raise Exception('Not valid %s' % each)
		return addr

	def _clean_from_addr(self, addr):
		if not addr:
			raise Exception('No from addresses')
		if not re.match(EMAIL_REGEX, addr):
			raise Exception('Not valid %s' % addr)
		return addr

	def run(self):
		return getattr(self, self.callback, None)(*self.args)

	def leave_request(self, leave):
		self.subject = LEAVE_REQUEST_SUBJECT
		self.msg = LEAVE_REQUEST_MSG % (
			leave.approver.name,
			leave.requester.name, 
			leave.type_of_leave.type_of_leave, 
			leave.start.strftime(DATETIME_INPUT_FORMATS[1]), 
			leave.end.strftime(DATETIME_INPUT_FORMATS[1])
		)
		return send_mail(
			self.subject, 
			self.msg, 
			self.from_addr,
			self.to_addr
		)
