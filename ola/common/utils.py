import calendar
import datetime

def get_value_from_request(request):
	value = request.GET
	if request.method == "POST":
		value = request.body
	return value

def get_month_end(month=datetime.datetime.today().month, year=datetime.datetime.today().year):
	return calendar.monthrange(year, month)[1]