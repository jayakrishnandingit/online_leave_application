from django.contrib.auth.decorators import user_passes_test

GROUP_NAME_MAP = {
	'COMPANY_ADMIN' : 'Company Admin',
	'LEAVE_APPROVER' : 'Leave Approver',
	'LEAVE_REQUESTER' : 'Leave Requester'
}

def group_required(*group_names):
	"""Requires user membership in at least one of the groups passed in."""
	def in_groups(u):
		if u.is_authenticated():
			if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
				return True
		return False
	return user_passes_test(in_groups, login_url='/')

class UserGroupManager(object):
	@staticmethod
	def check_user_group(user):
		groupDict = {}
		if not user.is_superuser:
			userGroup = user.groups.get()
			for key, value in GROUP_NAME_MAP.iteritems():
				groupDict.update({key : False})
				if userGroup.name == value:
					groupDict.update({key : True})
		return groupDict

	@staticmethod
	def is_company_admin(user):
		auth_group = UserGroupManager.check_user_group(user)
		if auth_group.get('COMPANY_ADMIN'):
			return True
		return False

	@staticmethod
	def can_approve_leave(user):
		auth_group = UserGroupManager.check_user_group(user)
		if auth_group.get('LEAVE_APPROVER'):
			return True
		return False

	@staticmethod
	def can_request_leave(user):
		auth_group = UserGroupManager.check_user_group(user)
		if auth_group.get('LEAVE_REQUESTER'):
			return True
		return False

	@staticmethod
	def has_leave_privilege(user):
		if UserGroupManager.can_approve_leave(user) or UserGroupManager.can_request_leave(user):
			return True
		return False
