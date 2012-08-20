$(document).ready(function(){
	$('a.external')
		.live('click', function() {
			window.open(this.href);
			return false;
		})
		.live('keypress', function(event) {
			if (event.keyCode == '13') {
				window.open(this.href);
				return false;
			}
		});

	$('#id_username').focus();
});
