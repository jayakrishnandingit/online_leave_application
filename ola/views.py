import json
from django import http
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from ola.common.permissions import UserGroupManager, GROUP_NAME_MAP
from django.views.generic import View
from leave.forms import LeaveForm

class HomeView(View):
	def get(self, request):
		auth_group = UserGroupManager.check_user_group(request.user)
		context = {
			'auth_group' : auth_group,
			'leave_form' : LeaveForm()
		}
		return render(request, 'ola/home.html', context)
