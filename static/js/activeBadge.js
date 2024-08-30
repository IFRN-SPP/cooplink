$(document).ready(function() {
  $('fieldset > div').first().addClass('d-flex gap-3');

  var legend = $('legend.form-label.requiredField');
  var badge = $('<span class="badge fs-6 fw-semibold text-bg-success" id="status_badge">ATIVA</span>');
  legend.append(badge);

  function updateBadge() {
      var checkedValue = $('input[name="active_choice"]:checked').val();
      if (checkedValue === 'true') {
          badge.text('ATIVA').removeClass('text-bg-warning').addClass('text-bg-success');
      } else if (checkedValue === 'false') {
          badge.text('INATIVA').removeClass('text-bg-success').addClass('text-bg-warning');
      }
  }

  updateBadge();

  $('input[name="active_choice"]').change(function() {
      updateBadge();
  });
});