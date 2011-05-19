$(document).ready(function() {
	var table = $('#changelist-main table');
	table.find('thead input[type=checkbox]').parent().addClass('narrow');
	table.find('tbody tr:last-child').addClass('last');
	table.find('tbody tr').find('td:first-child, th:first-child').addClass('first');
	table.find('tbody tr').find('td:last-child, th:last-child').addClass('last');
	table.find('tbody tr td').find("img[src$='icon-yes.gif']").parent()
		.addClass('bool').html('<img src="' + path_to_yes_icon + '" alt="True">');
	table.find('tbody tr td').find("img[src$='icon-no.gif']").parent()
		.addClass('bool').html('<img src="' + path_to_no_icon + '" alt="False">');
	table.find('tbody td.last').find('input[type=hidden]').parent()
		.hide().prev().addClass('last');
	$('#main-buttons input[type=submit]').click(function(){
		$('<input>').attr({
			type: 'hidden',
			name: $(this).attr('name'),
			value: $(this).attr('value')
		}).appendTo($('#changelist-main form'));
		$('#changelist-main form').submit();
	});
});
