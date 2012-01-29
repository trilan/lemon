$(document).ready(function() {
  var $menu = $('#b-admin-menu'),
      $menuHelper = $('<div class="b-admin-menu-helper"></div>').insertAfter($menu);
  $menu.children().hover(
    function() {
      var $span = $(this).children('span'),
          ulWidth = $(this).children('ul').outerWidth(),
          spanWidth = $span.outerWidth(),
          spanLeft  = $span.offset().left;
      $menuHelper.css({left: spanLeft + spanWidth, width: ulWidth - spanWidth}).show();
    },
    function() {
      $menuHelper.hide();
    }
  );
});
