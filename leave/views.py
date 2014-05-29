from django.shortcuts import render
from ola.common.permissions import UserGroupManager
from forms import LeaveForm
# Create your views here.
def index(request):
	auth_group = UserGroupManager.check_user_group(request.user)
	context = {
		'auth_group' : auth_group,
		'leave_form' : LeaveForm()
	}
	return render(request, 'leave/landing_page.html', context)