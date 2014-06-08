import copy
from ola.common.ajax import JSONParser
from ola.common.permissions import UserGroupManager, GROUP_NAME_MAP
from models import LeaveType
from subscriber.models import Subscriber
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

class LeaveTypeAjaxHandler(JSONParser):
	def get_all(self):
		logged_in_employee = Subscriber.objects.get(user=self.user)
		if not UserGroupManager.is_company_admin(self.user):
			raise UnauthorizedException('Access Violation')
		leave_types = LeaveType.objects.filter(client=logged_in_employee.client).order_by('created_on')
		serialized_objects = []
		for leave_type in leave_types:
			serialized_objects.append(leave_type)
		return self.respond(leave_types=serialized_objects)
