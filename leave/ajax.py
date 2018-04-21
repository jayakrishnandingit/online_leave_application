import copy
import threading
import datetime
from ola.common.ajax import JSONParser
from ola.common.utils import get_month_end
from ola.common.permissions import UserGroupManager, GROUP_NAME_MAP
from models import Leave, LeaveType, Holiday, LeaveBucket, LeaveStatus
from forms import LeaveForm, LeaveTypeForm, HolidayForm
from subscriber.models import Subscriber, NotificationAction, SubscriberNotification
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from ola.settings import DATE_INPUT_FORMATS
from mailer import SendNotification
from constants import NUMBER_OF_RECORDS_PER_PAGE, INITIAL_PAGE_NO

class LeaveAjaxHandler(JSONParser):
	def request_leave(self, form_values):
		logged_in_employee = Subscriber.objects.get(user=self.user)
		form = LeaveForm(logged_in_employee, form_values)
		if form.is_valid():
			leave = form.save(commit=False)
			leave.type_of_leave = LeaveType.objects.get(pk=form.cleaned_data['leave_type'])
			leave.requester = logged_in_employee
			leave.approver = Subscriber.objects.get(user__id__exact=form.cleaned_data['approver'])
			leave.status = LeaveStatus.PENDING
			leave.save()
			SendNotification([leave.approver.user.email], leave.requester.user.email, 'leave_request', leave).start()
			threading.Thread(target=self.leave_update_trigger, args=(leave, None)).start()
			return self.respond(is_saved=True, leave=leave.serialize())
		return self.respond(is_saved=False, errors=form.errors)

	def leave_update_trigger(self, new_leave, old_leave):
		if not old_leave:
			if new_leave.status == LeaveStatus.PENDING:
				SubscriberNotification(
					actor=new_leave.requester,
					action=NotificationAction.LEAVE_REQUESTED,
					recipient=new_leave.approver,
					has_read=False
				).save()
		return True

	def get_pending_approvals_for_subscriber(self, user_id, page_no=INITIAL_PAGE_NO, no_of_records=NUMBER_OF_RECORDS_PER_PAGE, show_all=False, **kwargs):
		logged_in_employee = Subscriber.objects.get(user=self.user)
		subscriber_to_get = Subscriber.objects.get(user__id__exact=user_id)

		if not (UserGroupManager.can_approve_leave(self.user) and logged_in_employee.id == subscriber_to_get.id):
			if not UserGroupManager.is_company_admin(self.user):
				return self.respond(is_saved=False, auth_errors='Permission Denied')

		pending_approvals = self._prepare_search(Leave.objects.filter(
			approver=subscriber_to_get,
			status__exact=LeaveStatus.PENDING
		).order_by('-created_on'), **kwargs)

		show_all = bool(int(show_all))
		prevPageNo = 0
		nextPageNo = 0
		current_page_number = 0
		num_of_pages = pending_approvals.count()
		if not show_all:
			paginator = Paginator(pending_approvals, no_of_records)
			try:
				pending_approvals = paginator.page(page_no)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				pending_approvals = paginator.page(1)
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				pending_approvals = paginator.page(paginator.num_pages)

			try:
				prevPageNo = pending_approvals.previous_page_number()
			except InvalidPage as e:
				prevPageNo = page_no
			try:
				nextPageNo = pending_approvals.next_page_number()
			except InvalidPage as e:
				nextPageNo = page_no
			current_page_number = pending_approvals.number
			num_of_pages = pending_approvals.paginator.num_pages

		serializedObjects = []
		for pending in pending_approvals:
			serializedObjects.append(pending.serialize(maxDepth=1))

		return self.respond(
			pending_approvals=serializedObjects,
			previous_page_number=prevPageNo,
			next_page_number=nextPageNo,
			current_page_number=current_page_number,
			num_of_pages=num_of_pages,
			no_of_records=no_of_records,
			subscriber=subscriber_to_get.serialize(maxDepth=1)
		)

	def get_subscriber_leave_requests(self, user_id, page_no=INITIAL_PAGE_NO, no_of_records=NUMBER_OF_RECORDS_PER_PAGE, show_all=False, **kwargs):
		auth_group = UserGroupManager.check_user_group(self.user)
		logged_in_employee = Subscriber.objects.get(user=self.user)
		subscriber_to_get = Subscriber.objects.get(user__id__exact=user_id)
		is_company_admin = UserGroupManager.is_company_admin(self.user)
		if not logged_in_employee.id == subscriber_to_get.id:
			if not is_company_admin:
				return self.respond(is_saved=False, auth_errors='Permission Denied')

		leaves = self._prepare_search(Leave.objects.filter(requester=subscriber_to_get).order_by('-created_on'), **kwargs)

		show_all = bool(int(show_all))
		prevPageNo = 0
		nextPageNo = 0
		current_page_number = 0
		num_of_pages = leaves.count()
		if not show_all:
			paginator = Paginator(leaves, no_of_records)
			try:
				leaves = paginator.page(page_no)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				leaves = paginator.page(1)
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				leaves = paginator.page(paginator.num_pages)

			try:
				prevPageNo = leaves.previous_page_number()
			except InvalidPage as e:
				prevPageNo = page_no
			try:
				nextPageNo = leaves.next_page_number()
			except InvalidPage as e:
				nextPageNo = page_no
			current_page_number = leaves.number
			num_of_pages = leaves.paginator.num_pages

		serializedObjects = []
		for leave in leaves:
			serializedObjects.append(leave.serialize(maxDepth=1))

		return self.respond(
			leaves=serializedObjects,
			previous_page_number=prevPageNo,
			next_page_number=nextPageNo,
			current_page_number=current_page_number,
			num_of_pages=num_of_pages,
			no_of_records=no_of_records,
			subscriber=subscriber_to_get.serialize(maxDepth=1)
		)

	def _prepare_search(self, leaves, **search_values):
		if search_values.get('status'):
			leaves = leaves.filter(status__exact=search_values['status'])
		if search_values.get('start_date_time'):
			leaves = leaves.filter(start__gte=datetime.datetime.strptime(search_values['start_date_time'], DATE_INPUT_FORMATS[0]))
		if search_values.get('end_date_time'):
			leaves = leaves.filter(start__lte=datetime.datetime.strptime(search_values['end_date_time'], DATE_INPUT_FORMATS[0]))
		return leaves

class LeaveTypeAjaxHandler(JSONParser):
	def get_all(self):
		logged_in_employee = Subscriber.objects.get(user=self.user)
		if not UserGroupManager.is_company_admin(self.user):
			raise UnauthorizedException('Access Violation')
		leave_types = LeaveType.objects.filter(client=logged_in_employee.client).order_by('created_on')
		serialized_objects = []
		for leave_type in leave_types:
			serialized_objects.append(leave_type.serialize())
		return self.respond(leave_types=serialized_objects)

	def save(self, form_values):
		logged_in_employee = Subscriber.objects.get(user=self.user)
		if not UserGroupManager.is_company_admin(self.user):
			raise UnauthorizedException('Access Violation')

		leave_type = LeaveType.objects.filter(pk=form_values.get('hidden_type_id')).first()
		old_leave_type = copy.copy(leave_type)
		form = LeaveTypeForm(form_values, instance=leave_type)
		if form.is_valid():
			leave_type = form.save(commit=False)
			leave_type.client = logged_in_employee.client
			leave_type.created_by = logged_in_employee
			leave_type.save()
			# we need to update leave bucket of each subscriber
			update_trigger = threading.Thread(target=self.leave_bucket_update_trigger, args=(leave_type, old_leave_type, logged_in_employee))
			update_trigger.start()
			return self.respond(is_saved=True, leave_type=leave_type.serialize())
		return self.respond(is_saved=False)

	def leave_bucket_update_trigger(self, new_leave_type, old_leave_type, logged_in_employee):
		if not old_leave_type:
			subscribers_to_update = Subscriber.objects.filter(client=new_leave_type.client)
			leave_buckets = []
			for subscriber in subscribers_to_update:
				leave_buckets.append(LeaveBucket(
					subscriber=subscriber,
					type_of_leave=new_leave_type,
					bucket=new_leave_type.no_of_leave,
					created_by=logged_in_employee
				))
			LeaveBucket.objects.bulk_create(leave_buckets)
		else:
			change_in_bucket = new_leave_type.no_of_leave - old_leave_type.no_of_leave
			if change_in_bucket:
				leave_buckets = LeaveBucket.objects.filter(type_of_leave=old_leave_type)
				for leave_bucket in leave_buckets:
					leave_bucket.bucket += change_in_bucket
					leave_bucket.save()
		return True

	def delete(self, ids_to_delete):
		logged_in_employee = Subscriber.objects.get(user=self.user)
		if not UserGroupManager.is_company_admin(self.user):
			raise UnauthorizedException('Access Violation')
		if Leave.objects.filter(type_of_leave__id__in=ids_to_delete).count() > 0:
			return self.respond(is_saved=False, errors='There are leaves bound to the leave type.')
		# if there aren't any leaves associated with the type, then
		# clear the subscribers' leave bucket and then
		# delete the type.
		LeaveBucket.objects.filter(type_of_leave__id__in=ids_to_delete).delete()
		LeaveType.objects.filter(id__in=ids_to_delete).delete()
		return self.respond(is_saved=True)

class HolidayAjaxHandler(JSONParser):
	def get_all(self, start, end):
		if not UserGroupManager.is_company_admin(self.user):
			raise UnauthorizedException('Access Violation')

		logged_in_employee = Subscriber.objects.get(user=self.user)
		if not start:
			start = datetime.datetime.today().replace(day=1).date()
		else:
			start = datetime.datetime.strptime(start, DATE_INPUT_FORMATS[0]).date()
		if not end:
			end = datetime.datetime.today().replace(day=get_month_end()).date()
		else:
			end = datetime.datetime.strptime(end, DATE_INPUT_FORMATS[0]).date()

		holidays = Holiday.objects.filter(
			client=logged_in_employee.client,
			start__gte=start,
			start__lte=end
		).order_by('start')
		serialized_objects = []
		for holiday in holidays:
			serialized_objects.append(holiday.serialize())
		return self.respond(holidays=serialized_objects)

	def save(self, form_values):
		if not UserGroupManager.is_company_admin(self.user):
			raise UnauthorizedException('Access Violation')
		logged_in_employee = Subscriber.objects.get(user=self.user)

		form = HolidayForm(form_values, instance=Holiday.objects.filter(pk=form_values.get('id')).first())
		if form.is_valid():
			holiday = form.save(commit=False)
			holiday.client = logged_in_employee.client
			holiday.created_by = logged_in_employee
			holiday.save()
			return self.respond(is_saved=True, holiday=holiday.serialize())
		return self.respond(is_saved=False, errors=form.errors)

	def delete(self, holiday_id):
		if not UserGroupManager.is_company_admin(self.user):
			raise UnauthorizedException('Access Violation')
		logged_in_employee = Subscriber.objects.get(user=self.user)

		Holiday.objects.get(pk=holiday_id).delete()
		return self.respond(is_saved=True)
