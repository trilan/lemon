$(document).ready(function(){
	$('#main-menu dl').hover(
		function(){
			//alert('!!!');
			var dl = $(this);
			var dt = dl.children('dt:first');
			var cont = dl.parent();
			cont.addClass('hover');
			if (dt.children('span').length == 0) {
				back = $(document.createElement('span'));
				back
					.appendTo(dt)
					.css({
						'background': 'white', // IE bug
						'opacity': '0',
						'filter': 'progid:DXImageTransform.Microsoft.Alpha(opacity=0);',
						'position': 'absolute',
						'display': 'block',
						'z-index': '-1'
						});
			}
			var cont = dl.parent();
			dt.css({
				'width': dt.width()+'px',
				'height': dt.height()+'px'
				});
			cont
				.css({
					'position': 'relative',
					'z-index': '10',
					'width': cont.width()+'px',
					'height': cont.height()+'px'
					})
				.addClass('open');
			dl
				.css('position', 'absolute')
				.css('z-index', '10')
				.addClass('ui-widget-header')
				.addClass('ui-corner-all');

			if (cont.get(0).tagName == 'LI') {
				dl.css({
					'top': '37px',
					'left': '5px'
					});
				dt.css({
					'position': 'absolute',
					'top': '-38px',
					'left': '-6px'
					});
				if (cont.width() < dl.width()) {
					back.width(dl.width());
				}
				else {
					back.width(cont.width());
				}
				back.css({
					'height': '3px',
					'top': '100%',
					'left': '5px'
					});
			}
			else {
				dl.css({
					'top': '-2px',
					'left': (cont.width() + 25) + 'px'
					});
				dt.css({
					'position': 'absolute',
					'top': '1px',
					'left': -(cont.width() + 17) + 'px'
					});
				back
					.height(cont.parent().height())
					.css({
						'width': '16px',
						'top': '0',
						'left': '100%'
						});
			}

			dl.children('dd:first').children('a:first').addClass('first');
			dl.children('dd:first').children('dl:first').children('dt:first').addClass('first');
			dl.children('dd:last').children('a:first').addClass('last');
			dl.children('dd:last').children('dl:first').children('dt:first').addClass('last');
			dl.children().css({
				'display': 'block',
				'z-index': '10'
			});

			return false;
		},
		function(){
			var dl = $(this);
			var dt = dl.children('dt:first');
			var cont = dl.parent();

			dl.children('dd').css({
				'display': 'none',
				'z-index': '0'
			});
			dl
				.css({
					'position': 'static',
					'top': '0',
					'left': '0'
					})
				.removeClass('ui-widget-header')
				.removeClass('ui-corner-all');
			dt.css({
				'position': 'relative',
				'z-index': '3',
				'display': 'block',
				'top': 'auto',
				'left': 'auto',
				'width': 'auto',
				'height': 'auto'
				});
			cont
				//.css('width', 'auto')
				.removeClass('open')
				.removeClass('hover');
		}
	);

	$('#main-menu li, #main-menu dd')
		.hover(
			function(){
				$(this).addClass('hover');
				$(this).children('dl').hover();
			},
			function(){
				$(this).removeClass('hover');
			}
		);
});
