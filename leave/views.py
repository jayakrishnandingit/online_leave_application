from django.shortcuts import render
from ola.common.permissions import UserGroupManager
# Create your views here.
def index(request):
	return render(request, 'leave/landing_page.html')