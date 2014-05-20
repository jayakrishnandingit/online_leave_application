function customSerializer(formId, findCheckboxes) {
   	var jquerySerializedArray = $('#' + formId).serializeArray();
   	var serializeObject = {};
   	$.each(jquerySerializedArray, function (index, dict) {
		serializeObject[dict.name] = dict.value;
   	});
   	if (findCheckboxes) {
		// update checkboxes
		$.each($('#' + formId + ' :checkbox'), function (index, elem) {
			serializeObject[$(elem).attr('name')] = $(elem).is(':checked');
	   	});
   	}
   	return serializeObject;
}

function compareDates(start, end, convert) {
	if (convert) {
		start = getDateFromString(start);
		end = getDateFromString(end);
	}
	result = start - end;
	return result;
}

function getFormattedDate(jsDateObj) {
	var day = jsDateObj.getDate();
	var month = jsDateObj.getMonth() + 1;
	var year = jsDateObj.getFullYear();
	return (day < 10 ? '0' + day : day) + '/' + (month < 10 ? '0' + month : month) + '/' + year;
}

function getUnixFormattedDate(jsDateObj) {
	var day = jsDateObj.getDate();
	var month = jsDateObj.getMonth() + 1;
	var year = jsDateObj.getFullYear();
	return (year + '-'+ (month < 10 ? '0' + month : month) + '-' + ('01'));
}

function getDateTimeFromString(dateString) {
	var dateTimeSplit = dateString.split(' ');
	var dateOnly = dateTimeSplit[0].split('/');
	var timeOnly = dateTimeSplit[1].split(':');

	var day = parseInt(dateOnly[0]);
	var month = parseInt(dateOnly[1]) - 1; // since javascript Date month is zero indexed.
	var year = parseInt(dateOnly[2]);

	var hour = timeOnly.length > 0 ? parseInt(timeOnly[0]) : 0;
	var minute = timeOnly.length > 1 ? parseInt(timeOnly[1]) : 0;
	var second = timeOnly.length > 2 ? parseInt(timeOnly[2]) : 0;
	return new Date(year, month, day, hour, minute, second);
}

function getDateFromString(dateString) {
	var dateSplit = dateString.split('/');
	var day = parseInt(dateSplit[0]);
	var month = parseInt(dateSplit[1]) - 1; // since javascript Date month is zero indexed.
	var year = parseInt(dateSplit[2]);
	return new Date(year, month, day);
}

function calcDate(date1,date2) {
	var diff_in_ms = Math.floor(date2.getTime() - date1.getTime());
	var day_ms = 1000* 60 * 60 * 24;
	var hour_ms = 1000 * 60 * 60;
	var min_ms = 1000 * 60;

	var minutes = Math.floor(diff_in_ms/ min_ms);
	var hours = Math.floor(diff_in_ms/ hour_ms);
	var days = Math.floor(diff_in_ms/day_ms);
	var months = Math.abs(date2.getMonth() - date1.getMonth());
	var years = Math.abs(date2.getFullYear() - date1.getFullYear());

	return {
		'minutes' : minutes,
		'hours' : hours,
		'days' : days,
		'months' : months,
		'years' : years
	};
}

function setFormFieldValues(jsonObj, formId) {
	$.each($('#' + formId + ' :input').not(':input[type=button], :input[type=submit], :input[type=reset]'), function(index, element) {
		$(element).val(jsonObj[$(element).attr('name')]);
	});
	$.each($('#' + formId + ' select'), function(index, element) {
		$(element).val(jsonObj[$(element).attr('name')]);
	});
}

function setHtmlValues(jsonObj, boolShdBe, nullValueString) {
	for (var key in jsonObj) {
		if ($('#' + key)) {
			if (typeof(jsonObj[key]) == 'boolean') {
				jsonObj[key] = boolShdBe[jsonObj[key]];
			} else if (!jsonObj[key] || jsonObj[key] == null || jsonObj[key] == 'undefined') {
				jsonObj[key] = '<span class="inActiveValue">' + nullValueString + '</span>';
			}
			$('#' + key).html(jsonObj[key]);
		}
	}
}

function showFormErrors(jsonObj, formId) {
	$.each($('#' + formId + ' span.error'), function (index, element) {
		if (jsonObj[$(element).attr('name')]) {
			$(element).text(jsonObj[$(element).attr('name')][0]);
		}
	});
}

function clearFormErrors(formId) {
	$.each($('#' + formId + ' span.error'), function (index, element) {
		$(element).text('');
	});
}

function clearFormFieldValues(formElement, notClearClass) {
	$.each($('#' + formElement + ' :input').not(':input[type=button], :input[type=submit], :input[type=reset], .' + notClearClass), function(index, element) {
		if ($(element).is(':checkbox') || $(element).is(':radio')) {
			$(element).prop('checked', '');
		} else {
			$(element).val('');
		}
	});
}

function showSaveSuccess(id) {
	$.each($('.content'), function (index, elem) {
		$(elem).hide();
	});
	$('#' + id).show();
	$('#alertSuccess').fadeIn(1000);
	setTimeout(function () {$("#alertSuccess").fadeOut(1000);}, 5000);
}

function showSaveError(id) {
	$.each($('.content'), function (index, elem) {
		$(elem).hide();
	});
	$('#' + id).show();
	$('#alertError').fadeIn(1000);
	setTimeout(function () {$("#alertError").fadeOut(1000);}, 4000);
}

function populateTemplate(container, tmplt, values, options) {
	if ($('#' + container)) {
		$('#' + container).loadTemplate($('#' + tmplt), values, options);
	}
}

function showLoadingDiv(hide) {
	if (!hide) {
		$('.transparentDiv').show();
		$('.loadingContainer').show();
	} else {
		$('.loadingContainer').hide();
		$('.transparentDiv').hide();
	}
}