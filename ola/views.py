from django import http
from django.views.decorators.csrf import csrf_exempt
import json
from config import RestApiMap

@csrf_exempt
def rest_api_handler(request):
	args = json.loads(get_value_from_request(request))
	ajaxMainClass = RestApiMap.get(args.pop())()
	ajaxMainClass.httpRequest = request
	ajaxMainClass.user = request.user
	funtionToCall = getattr(ajaxMainClass, args.pop(), None)
	if not funtionToCall:
		return http.Http404

	responseValues = funtionToCall(*args)
	response = http.HttpResponse()
	response.status_code = 200
	response.write(responseValues)
	response['Content-Type'] = 'application/json'
	return response

def get_value_from_request(request):
	value = request.GET
	if request.method == "POST":
		value = request.body
	print value
	return value
