$(document).ready(function() {
  $('button.deletelink').click(function() {
    window.location = 'delete/';
    return false;
  });
  $('.b-admin-form-table-header').each(function() {
    $('th:first', $(this)).addClass('first');
    $('th:last', $(this)).addClass('last');
  });
});
