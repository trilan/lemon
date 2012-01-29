$(document).ready(function() {
  $('#action-toggle').click(function() {
    if ($(this).attr('checked')) {
      $('.action-select').attr('checked', 'checked');
    } else {
      $('.action-select').removeAttr('checked');
    }
  });
  $('.action-select').click(function() {
    if ($(this).not(':checked').size()) {
      $('#action-toggle').removeAttr('checked');
    } else {
      $('#action-toggle').attr('checked', 'checked');
    }
  });
  $('select[name=action]').change(function() {
    $('input[name=action]').val($(this).val());
  });
  $('#b-admin-changelist-actions button[type=submit]').click(function() {
    $('#b-admin-changelist-main form').submit();
  });
});
