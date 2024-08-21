$(document).ready(function() {

  const badge = $('#status_badge');
  const activeTrue = $('#id_active_true');
  const activeFalse = $('#id_active_false');

  function updateBadge() {
    if (activeTrue.is(':checked')) {
        badge.removeClass('text-bg-warning').addClass('text-bg-success').text('ATIVA')
    } else {
        badge.removeClass('text-bg-success').addClass('text-bg-warning').text('INATIVA')
    }
  }

  activeTrue.change(function() {
    if ($(this).is(':checked')) {
        activeFalse.prop('checked', false)
    } else {
      activeTrue.prop('checked', true)
    }
    updateBadge()
  })
  activeFalse.change(function() {
    if ($(this).is(':checked')) {
        activeTrue.prop('checked', false)
    } else {
      activeFalse.prop('checked', true)
    }
    updateBadge()
  })

  updateBadge()
});