// Based on http://code.djangoproject.com/browser/django/trunk/django/conf/admin_media/js/admin/DateTimePicker.js?rev=453
// and http://code.djangoproject.com/browser/django/trunk/django/conf/admin_media/js/admin/calendar.js?rev=453


lemon_media_prefix = '';
week_start = 1; // Monday

// CalendarNamespace -- Provides a collection of HTML calendar-related helper functions
var CalendarNamespace = {
	monthsOfYear: gettext('January February March April May June July August September October November December').split(' '),
	daysOfWeek: gettext('S M T W T F S').split(' '),
	getDaysInMonth: function(month, year) {
		if (month==1 || month==3 || month==5 || month==7 || month==8 || month==10 || month==12) {
			return 31;
		}
		if (month==4 || month==6 || month==9 || month==11) {
			return 30;
		}
		if (month==2 && (((year % 4)==0) && ((year % 100)!=0) || ((year % 400)==0))) {
			return 29;
		}
		return 28;
	},
	draw: function(month, year, num, callback) { // month = 1-12, year = 1-9999
		month = parseInt(month);
		year = parseInt(year);
		var div_id = DateTimePicker.calendarDivName2 + num;
		var calDiv = $('#'+div_id);
		calDiv.children().remove();
		calDiv.attr('num', num);

		var calHeader = $(document.createElement('caption'));
		calHeader
			.addClass('ui-widget-header ui-corner-all')
			.append('<h2 class="ui-datepicker-title">' + CalendarNamespace.monthsOfYear[month-1] + ' ' + year + '</h2>')

		var calTable = $(document.createElement('table'));
		var tableBody = $(document.createElement('tbody'));
		calTable
			.addClass('ui-widget ui-widget-content ui-corner-all') //ui-helper-clearfix ui-helper-hidden-accessible
			.append(calHeader)
			.append(tableBody);

		// next-prev links
		var cal_nav_prev = $(document.createElement('a'));
		cal_nav_prev
			.append('<span class="ui-icon ui-icon-circle-triangle-w"><</span>')
			.appendTo(calHeader)
			.addClass('calendarnav-previous')
			.addClass('ui-datepicker-next ui-corner-all')
			.css('cursor', 'pointer')
			.hover(
				function() {
					$(this).addClass('ui-state-hover');
				},
				function() {
					$(this).removeClass('ui-state-hover');
				}
			)
			.click(function() {
				DateTimePicker.drawPrev(calDiv.attr('num'));
				return false;
			});

		var cal_nav_next = $(document.createElement('a'));
		cal_nav_next
			.append('<span class="ui-icon ui-icon-circle-triangle-e">></span>')
			.appendTo(calHeader)
			.addClass('calendarnav-next')
			.addClass('ui-datepicker-next ui-corner-all')
			.css('cursor', 'pointer')
			.hover(
				function() {
					$(this).addClass('ui-state-hover');
				},
				function() {
					$(this).removeClass('ui-state-hover');
				}
			)
			.click(function() {
				DateTimePicker.drawNext(calDiv.attr('num'));
				return false;
			});

		// Draw days-of-week header
		var tableRow = $(document.createElement('tr'));
		tableRow.appendTo(tableBody);
		for (var i = week_start; i < 7; i++) {
			tableRow.append('<th>'+ CalendarNamespace.daysOfWeek[i] +'</th>');
		}
		for (var i = 0; i < week_start; i++) {
			tableRow.append('<th>'+ CalendarNamespace.daysOfWeek[i] +'</th>');
		}

		var startingPos = new Date(year, month-1, 1).getDay();
		var days = CalendarNamespace.getDaysInMonth(month, year);

		// Draw blanks before first of month
		var tableRow = $(document.createElement('tr'));
		tableRow.appendTo(tableBody);
		for (var i = week_start; i < startingPos; i++) {
			var _cell = $(document.createElement('td'));
			_cell
				.appendTo(tableRow)
				.css('background-color', '#f3f3f3');
		}

		// Draw days of month
		var currentDay = 1;
		for (var i = startingPos; currentDay <= days; i++) {
			if (i%7 == week_start && currentDay != 1) {
				var tableRow = $(document.createElement('tr'));
				tableRow.appendTo(tableBody);
			}
			var _cell = $(document.createElement('td'));
			_cell
				.appendTo(tableRow)
				.append('<a class="ui-state-default" href="javascript:void(' + callback + '('+year+','+month+','+currentDay+'));">' + currentDay + '</a>');
			currentDay++;
		}
		$('a.ui-state-default', calTable)
			.hover(
				function(){
					$(this).addClass('ui-state-hover');
				},
				function(){
					$(this).removeClass('ui-state-hover');
				}
			);
			/*.click(function(){
				$('.ui-state-active', calTable).removeClass('ui-state-active');
				$(this).addClass('ui-state-active');
			});*/
			
		

		// Draw blanks after end of month (optional, but makes for valid code)
		while (tableRow.children().length < 7) {
			var _cell = $(document.createElement('td'));
			_cell
				.appendTo(tableRow)
				.css('background-color', '#f3f3f3');
		}

		calDiv.append(calTable);
	}
}


// Calendar -- A calendar instance
function Calendar(div_id, callback) {
	// div_id (string) is the ID of the element in which the calendar will
	//	 be displayed
	// callback (string) is the name of a JavaScript function that will be
	//	 called with the parameters (year, month, day) when a day in the
	//	 calendar is clicked
	this.div_id = div_id;
	this.callback = callback;
	this.today = new Date();
	this.currentMonth = this.today.getMonth() + 1;
	this.currentYear = this.today.getFullYear();
}
Calendar.prototype = {
	drawCurrent: function() {
		CalendarNamespace.draw(this.currentMonth, this.currentYear, this.div_id, this.callback);
	},
	drawDate: function(month, year) {
		this.currentMonth = month;
		this.currentYear = year;
		this.drawCurrent();
	},
	drawPreviousMonth: function() {
		if (this.currentMonth == 1) {
			this.currentMonth = 12;
			this.currentYear--;
		}
		else {
			this.currentMonth--;
		}
		this.drawCurrent();
	},
	drawNextMonth: function() {
		if (this.currentMonth == 12) {
			this.currentMonth = 1;
			this.currentYear++;
		}
		else {
			this.currentMonth++;
		}
		this.drawCurrent();
	}
}


// Inserts shortcut buttons after all of the following:
//	 <input type="text" class="vDateField">
//	 <input type="text" class="vTimeField">


var DateTimePicker = {
	calendars: [],
	calendarInputs: [],
	clockInputs: [],
	calendarDivName1: 'calendarbox', // name of calendar <div> that gets toggled
	calendarDivName2: 'calendarin',  // name of <div> that contains calendar
	calendarLinkName: 'calendarlink',// name of the link that is used to toggle
	clockDivName:	 'clockbox',	// name of clock <div> that gets toggled
	clockLinkName:	'clocklink',	// name of the link that is used to toggle
	// Add clock widget to a given field
	addClock: function(inp) {
		var num = DateTimePicker.clockInputs.length;
		DateTimePicker.clockInputs[num] = inp;

		// Shortcut links (clock icon and "Now" link)
		var now_link = $(document.createElement('a'));
		now_link
			.attr('href', 'javascript:var d=new Date(); DateTimePicker.handleClockQuicklink('+num+', (d.getHours()<10?0:\'\') + d.getHours() + \':\' + (d.getMinutes()<10?0:\'\') + d.getMinutes() + \':\' + (d.getSeconds()<10?0:\'\') + d.getSeconds());')
			.append(document.createTextNode(gettext('Now')));
		var clock_link = $(document.createElement('img'));
		clock_link
			.attr('id', DateTimePicker.clockLinkName + num)
			.attr('src', lemon_media_prefix+'images/icon_clock.gif')
			.attr('alt', gettext('Clock'))
			.css('cursor', 'pointer')
			.click(function() {
				var clock_link = $(this);
				var num = parseInt(clock_link.attr('id').replace(DateTimePicker.clockLinkName, ''));
				var clock_box = $('#'+DateTimePicker.clockDivName+num);
			
				clock_box
					.css('right', '-9.7em')
					.css('top', '-5em')
					.css('display', 'block'); // show the clock box
				if ('\v' != 'v') {
				    $('#container').click(function() {
					    $(this).click(function() {
						    DateTimePicker.dismissClock(num);
						    return true;
					    });
					    return true;
				    });
				}
			});
		var shortcuts_span = $(document.createElement('span'));
		shortcuts_span
			.css('display', 'inline-block')
			.css('position', 'relative')
			.insertAfter(inp)
			.append(document.createTextNode('\240'))
			.append(now_link)
			.append(document.createTextNode('\240|\240'))
			.append(clock_link);

		// Create clock link div
		//
		// Markup looks like:
		// <div id="clockbox1" class="clockbox module">
		//	 <h2>Choose a time</h2>
		//	 <ul class="timelist">
		//		 <li><a href="#">Now</a></li>
		//		 <li><a href="#">Midnight</a></li>
		//		 <li><a href="#">6 a.m.</a></li>
		//		 <li><a href="#">Noon</a></li>
		//	 </ul>
		//	 <p class="calendar-cancel"><a href="#">Cancel</a></p>
		// </div>

		var clock_box = $(document.createElement('div'));
		clock_box
			.attr('id', DateTimePicker.clockDivName + num)
			.addClass('clockbox module')
			.addClass('ui-widget ui-widget-content ui-corner-all')
			.css('display', 'none')
			.css('position', 'absolute')
			.css('z-index', '2')
			.append('<h2 class="ui-datepicker-header ui-widget-header ui-helper-clearfix ui-corner-all">'+gettext('Choose a time')+'</h2>')
			.appendTo($('#' + DateTimePicker.clockLinkName + num).parent());
		
		time_list = $(document.createElement('ul'));
		time_list
			.appendTo(clock_box)
			.addClass('timelist')
			.append('<li><a class="ui-state-default" href="javascript:var d=new Date(); DateTimePicker.handleClockQuicklink('+num+', (d.getHours()<10?0:\'\') + d.getHours() + \':\' + (d.getMinutes()<10?0:\'\') + d.getMinutes() + \':\' + (d.getSeconds()<10?0:\'\') + d.getSeconds());">'+gettext("Now")+'</a></li>')
			.append('<li><a class="ui-state-default" href="javascript:DateTimePicker.handleClockQuicklink('+num+', \'00:00:00\');">'+gettext("Midnight")+'</a></li>')
			.append('<li><a class="ui-state-default" href="javascript:DateTimePicker.handleClockQuicklink('+num+', \'06:00:00\');">'+gettext("6 a.m.")+'</a></li>')
			.append('<li><a class="ui-state-default" href="javascript:DateTimePicker.handleClockQuicklink('+num+', \'12:00:00\');">'+gettext("Noon")+'</a></li>');
		$('a.ui-state-default', time_list).hover(
			function(){
				$(this).addClass('ui-state-hover');
			},
			function(){
				$(this).removeClass('ui-state-hover');
			}
		);
		
		cancel_p = $(document.createElement('p'));
		cancel_p
			.appendTo(clock_box)
			.addClass('calendar-cancel')
			.append('<a href="javascript:DateTimePicker.dismissClock('+num+');">'+gettext('Cancel')+'</a>');
	},
	dismissClock: function(num) {
		$('#'+DateTimePicker.clockDivName + num).css('display', 'none');
		$('#container').unbind('click');
	},
	handleClockQuicklink: function(num, val) {
		DateTimePicker.clockInputs[num].attr('value', val);
		DateTimePicker.dismissClock(num);
	},
	// Add calendar widget to a given field.
	addCalendar: function(inp) {
		var num = DateTimePicker.calendars.length;

		DateTimePicker.calendarInputs[num] = inp;

		// Shortcut links (calendar icon and "Today" link)
		var today_link = $(document.createElement('a'));
		today_link
			.attr('href', 'javascript:DateTimePicker.handleCalendarQuickLink(' + num + ', 0);')
			.append(document.createTextNode(gettext('Today')));
		var cal_link = $(document.createElement('img'));
		cal_link
			.attr('id', DateTimePicker.calendarLinkName + num)
			.attr('src', lemon_media_prefix+'images/icon_calendar.gif')
			.attr('alt', gettext('Calendar'))
			.css('cursor', 'pointer')
			.click(function() {
				var cal_link = $(this);
				var num = parseInt(cal_link.attr('id').replace(DateTimePicker.calendarLinkName, ''));
				var cal_box = $('#'+DateTimePicker.calendarDivName1+num);
				var inp = DateTimePicker.calendarInputs[num];

				// Determine if the current value in the input has a valid date.
				// If so, draw the calendar with that date's year and month.
				if (inp.attr('value')) {
					var date_parts = inp.attr('value').split('-');
					var year = date_parts[0];
					var month = parseFloat(date_parts[1]);
					if (year.match(/\d\d\d\d/) && month >= 1 && month <= 12) {
						DateTimePicker.calendars[num].drawDate(month, year);
					}
				}

				cal_box
					.css('right', '-16.5em')
					.css('top', '-7em')
					.css('display', 'block');
				if ('\v' != 'v') {
				    $('#container').click(function() {
    					$(this).click(function() {
    						DateTimePicker.dismissCalendar(num);
    						return true;
    					});
    					return true;
    				});
    			}
			});
		var shortcuts_span = $(document.createElement('span'));
		shortcuts_span
			.css('display', 'inline-block')
			.css('position', 'relative')
			.insertAfter(inp)
			.append(document.createTextNode('\240'))
			.append(today_link)
			.append(document.createTextNode('\240|\240'))
			.append(cal_link);

		// Create calendarbox div.
		//
		// Markup looks like:
		//
		// <div id="calendarbox3" class="calendarbox module">
		//	 <h2>
		//			<a href="#" class="link-previous">&lsaquo;</a>
		//			<a href="#" class="link-next">&rsaquo;</a> February 2003
		//	 </h2>
		//	 <div class="calendar" id="calendarin3">
		//		 <!-- (cal) -->
		//	 </div>
		//	 <div class="calendar-shortcuts">
		//		  <a href="#">Yesterday</a> | <a href="#">Today</a> | <a href="#">Tomorrow</a>
		//	 </div>
		//	 <p class="calendar-cancel"><a href="#">Cancel</a></p>
		// </div>
		var cal_box = $(document.createElement('div'));
		cal_box
			.css('display', 'none')
			.css('position', 'absolute')
			.addClass('calendarbox module')
			.addClass('ui-datepicker ui-widget ui-widget-content ui-corner-all')
			.attr('id', DateTimePicker.calendarDivName1 + num)
			.appendTo($('#' + DateTimePicker.calendarLinkName + num).parent());

		// main box
		var cal_main = $(document.createElement('div'));
		cal_main
			.attr('id', DateTimePicker.calendarDivName2 + num)
			.addClass('calendar')
			.appendTo(cal_box);
		DateTimePicker.calendars[num] = new Calendar(num, DateTimePicker.handleCalendarCallback(num));
		DateTimePicker.calendars[num].drawCurrent();

		// calendar shortcuts
		var shortcuts = $(document.createElement('div'));
		shortcuts
			.appendTo(cal_box)
			.addClass('calendar-shortcuts')
			.append('<a href="javascript:DateTimePicker.handleCalendarQuickLink(' + num + ', -1);">'+gettext('Yesterday')+'</a>')
			.append(document.createTextNode('\240|\240'))
			.append('<a href="javascript:DateTimePicker.handleCalendarQuickLink(' + num + ',  0);">'+gettext('Today')+'</a>')
			.append(document.createTextNode('\240|\240'))
			.append('<a href="javascript:DateTimePicker.handleCalendarQuickLink(' + num + ', +1);">'+gettext('Tomorrow')+'</a>');

		// cancel bar
		var cancel_p = $(document.createElement('p'));
		cancel_p
			.appendTo(cal_box)
			.addClass('calendar-cancel')
			.append('<a href="javascript:DateTimePicker.dismissCalendar(' + num + ');">'+gettext('Cancel')+'</a>');
	},
	dismissCalendar: function(num) {
		$('#'+DateTimePicker.calendarDivName1+num).css('display', 'none');
		$('#container').unbind('click');
	},
	drawPrev: function(num) {
		DateTimePicker.calendars[num].drawPreviousMonth();
	},
	drawNext: function(num) {
		DateTimePicker.calendars[num].drawNextMonth();
	},
	handleCalendarCallback: function(num) {
		return "function(y, m, d) { \
					DateTimePicker.calendarInputs["+num+"].attr('value', y+'-'+(m<10?'0':'')+m+'-'+(d<10?'0':'')+d); \
					$('#'+DateTimePicker.calendarDivName1+"+num+").css('display', 'none'); \
				 }";
	},
	handleCalendarQuickLink: function(num, offset) {
		var d = new Date();
		d.setDate(d.getDate() + offset)
		DateTimePicker.calendarInputs[num].attr('value', d.getFullYear()+'-'+(d.getMonth() < 9 ? 0 : '')+(d.getMonth()+1)+'-'+(d.getDate() < 10 ? 0 : '')+d.getDate());
		DateTimePicker.dismissCalendar(num);
	}
}

$.fn.datepicker = function(options){
	DateTimePicker.addCalendar(this);
}

$.fn.timepicker = function(options){
	DateTimePicker.addClock(this);
}

$(document).ready(function() {
	// Deduce lemon_media_prefix by looking at the <script>s in the
	// current document and finding the URL of *this* module.
	var scripts = $('script');
	for (var i=0; i<scripts.length; i++) {
		if (scripts[i].src.match(/jquery\.datetimepicker/)) {
			var idx = scripts[i].src.indexOf('js/jquery.datetimepicker');
			lemon_media_prefix = scripts[i].src.substring(0, idx);
			break;
		}
	}

	$('input.vTimeField').each(function() {
		$(this).timepicker();
	});
	$('input.vDateField').each(function() {
		$(this).datepicker();
	});
});

