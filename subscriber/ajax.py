from ola.common.ajax import JSONParser
from ola.common.permissions import UserGroupManager, GROUP_NAME_MAP
from client.forms import ClientForm
from forms import SubscriberCreationForm
from models import Subscriber
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

class SubscriberAjaxHandler(JSONParser):
	def do_registration(self, form_values):
		client_form = ClientForm(form_values)
		user_form = UserCreationForm(form_values)
		subscriber_form = SubscriberCreationForm(form_values)
		subscriber_form.need_to_check_leave = False
		if client_form.is_valid() and user_form.is_valid() and subscriber_form.is_valid():
			client = client_form.save(commit=False)
			client.payment_status = 0 # no payment, not so far.
			client.save()
			user = user_form.save(commit=False)
			user.email = subscriber_form.cleaned_data['email']
			user.first_name = subscriber_form.cleaned_data['first_name']
			user.last_name = subscriber_form.cleaned_data['last_name']
			user.is_active = True
			user.is_staff = False
			user.save()
			user_groups = [Group.objects.get(name__exact=GROUP_NAME_MAP['COMPANY_ADMIN'])]
			user.groups.add(*user_groups)
			subscriber = Subscriber(
				user=user,
				client=client,
				no_of_leave_remaining=0
			)
			subscriber.save()
			return self.respond(is_saved=True)
		return self.respond(
			is_saved=False, 
			client_form_errors=client_form.errors,
			user_form_errors=user_form.errors,
			subscriber_form_errors=subscriber_form.errors
		)

	def get_all(self, page_no, no_of_records, show_all):
		auth_group = UserGroupManager.check_user_group(self.user)
		if not UserGroupManager.is_company_admin(self.user):
			raise UnauthorizedException('Access Violation')
		logged_in_employee = Subscriber.objects.get(user=self.user)
		subscribers = Subscriber.objects.filter(client__id__exact=logged_in_employee.client.id).order_by('-created_on')

		prevPageNo = 0
		nextPageNo = 0
		current_page_number = 0
		num_of_pages = subscribers.count()
		if not show_all:
			paginator = Paginator(subscribers, no_of_records)
			try:
				subscribers = paginator.page(page_no)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				subscribers = paginator.page(1)
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				subscribers = paginator.page(paginator.num_pages)

			try:
				prevPageNo = subscribers.previous_page_number()
			except InvalidPage as e:
				prevPageNo = page_no
			try:
				nextPageNo = subscribers.next_page_number()
			except InvalidPage as e:
				nextPageNo = page_no
			current_page_number = subscribers.number
			num_of_pages = subscribers.paginator.num_pages

		serializedObjects = []
		for subscriber in subscribers:
			serializedObjects.append(subscriber.serialize(maxDepth=1))

		return self.respond(
			subscribers=serializedObjects,
			previous_page_number=prevPageNo,
			next_page_number=nextPageNo,
			current_page_number=current_page_number,
			num_of_pages=num_of_pages,
			nor=no_of_records
		)