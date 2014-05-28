def get_value_from_request(request):
	value = request.GET
	if request.method == "POST":
		value = request.body
	return value