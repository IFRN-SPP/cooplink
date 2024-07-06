$(document).ready(function() {
  var password = $('[id^=div_id_password]')
  var newPassword = $('[id^=div_id_new_password]')
  var confirmPassword = $('[id^=div_id_confirm_password]')
  var divList = []

  if (password.length) {divList.push(password);}
  if (newPassword.length) {divList.push(newPassword);}
  if (confirmPassword.length) {divList.push(confirmPassword);}

  divList.forEach(function(div) {
    div.each(function(index) {
      var label = $(this).find('label');
      var input = $(this).find('input');

      if (label.length && input.length) {
        var passwordContainer = $('<div class="password-container input-group"></div>');
        input.detach().appendTo(passwordContainer);
        passwordContainer.insertAfter(label);

        var showPasswordButton =  $(`
        <button type="button" class="btn btn-outline-success" title="Mostrar Senha" id="id_btn_password${index}">
            <i class="bi bi-eye-slash-fill"></i>
        </button>
        `);

        showPasswordButton.insertAfter(input);
        showPasswordButton.click(function() {
          var currentType = input.attr('type');
          if (currentType === 'password') {
              input.attr('type', 'text');
              $(this).find('i').removeClass('bi-eye-slash-fill').addClass('bi-eye-fill');
          } else {
              input.attr('type', 'password');
              $(this).find('i').removeClass('bi-eye-fill').addClass('bi-eye-slash-fill');
            }
        });
        //passwordContainer.append(showPasswordButton);
      }
    });
  });
});
