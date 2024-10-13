function processAlerts(container) {
  const alerts = container.querySelectorAll('.alert');

  alerts.forEach(alert => {
    if (!alert.dataset.timeoutSet) {
      setTimeout(() => {
        $(alert).fadeTo(2000, 500).slideUp(500, function() {
          $(alert).slideUp(500);
          alert.remove();
        });
      }, 2500);
      alert.dataset.timeoutSet = true;
    }
  });
}

function monitorAlertContainers() {
  const idMessagesContainer = document.getElementById('id-messages');
  const ajaxMessagesContainer = document.getElementById('ajax-messages');

  if (idMessagesContainer) processAlerts(idMessagesContainer);
  if (ajaxMessagesContainer) processAlerts(ajaxMessagesContainer);
}

setInterval(monitorAlertContainers, 1000);