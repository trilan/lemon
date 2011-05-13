$(document).ready(function() {
  $('button.deletelink').click(function() {
    window.location = 'delete/';
    return false;
  });
  $('div.tabular_group thead tr').each(function() {
    $('th:first', $(this)).addClass('first');
    $('th:last', $(this)).addClass('last');
  });
});
