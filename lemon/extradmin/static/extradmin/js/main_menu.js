$(document).ready(function() {
  var $main_menu = $('#main-menu'),
      $main_menu_helper = $('<div class="main-menu-helper"></div>').insertAfter($main_menu);
  $main_menu.children().hover(
    function() {
      var $span = $(this).children('span'),
          ul_width = $(this).children('ul').outerWidth(),
          span_width = $span.outerWidth(),
          span_left  = $span.offset().left;
      $main_menu_helper.css({
        left: span_left + span_width,
        width: ul_width - span_width
      }).show();
    },
    function() {
      $main_menu_helper.hide();
    }
  );
});
