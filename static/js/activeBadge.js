$(document).ready(function() {
  const checkbox = $('#id_active');
  var span = $('<span class="badge fs-6 fw-semibold pointer text-bg-warning" id="status_badge"></span>')

  $('#div_id_active').each(function(){
    var label = $(this).find('label')
    if (label){
      $(span).appendTo(label);
    }
  })

  badge = $('#status_badge')
  function updateBadge() {
      if (checkbox.is(':checked')) {
          badge.removeClass('text-bg-warning').addClass('text-bg-success').text('ATIVA');
      } else {
          badge.removeClass('text-bg-success').addClass('text-bg-warning').text('INATIVA');
      }
  }

  updateBadge();
  checkbox.change(updateBadge);

});