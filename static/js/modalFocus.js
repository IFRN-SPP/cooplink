$(document).ready(function() {
  $('.modal').on('shown.bs.modal', function() {
    $(this).find('input:visible:first').focus();
  });
});
