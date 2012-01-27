$(function() {
  $('.b-admin-form-field select')
    .width(function(index, width) { return $(this).attr('multiple') ? width + 150 : width + 50; })
    .chosen({disable_search_threshold: 50});
});
