from ola.common.config import BaseEnum

class LeaveStatusEnum(BaseEnum):
	def __init__(self, *args, **kwargs):
		self.DENIED = 0
		self.APPROVED = 1
