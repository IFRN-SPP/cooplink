$(function() {
  // Função para obter produtos relacionados à chamada selecionada
  var getProducts = function() {
    var callId = $(this).val(); // Obtenha o ID da chamada selecionada
    // Capture todos os campos de seleção de produtos
    var productSelects = $('[id^=id_call_products-]');
    // Faça uma solicitação AJAX para obter os produtos relacionados à chamada selecionada
    $.ajax({
      url: '/get_products/', // URL da sua view para obter os produtos
      type: 'GET',
      data: {'call_id': callId}, // Passe o ID da chamada como parâmetro
      success: function(data) {
        // Limpe e atualize as opções de produtos em todos os campos de seleção
        productSelects.each(function() {
          var currentSelect = $(this);
          currentSelect.empty();
          // Adicione as opções de produtos dinamicamente
          $.each(data.products, function(index, product) {
            currentSelect.append($('<option>', {
              value: product.id,
              text: product.text,
            }));
          });
        });
      }
    });
  };

  var getCalls = function() {
    var institutionId = $(this).val();
    var callSelects = $('#id_call');
    $.ajax({
      url: '/get_calls/',
      type: 'GET',
      data: {'institution_id': institutionId},
      success: function(data) {
        callSelects.each(function() {
          var currentSelect = $(this);
          currentSelect.empty();

          $.each(data.calls, function(index, call) {
            currentSelect.append($('<option>', {
              value: call.id,
              text: call.text,
            }));
          });
        });

       getProducts.call($('#id_call'))
      }
    });
  };

  $('#id_institution').on('change', getCalls);
  // Adicione um evento de mudança a todos os campos de seleção da chamada
  $('#id_call').on('change', getProducts);
  // Evento de clique no botão "Adicionar linha"
  $('.add-row').click(function() {
    var callId = $('#id_call').val();
    // Se um valor estiver selecionado na chamada, chame a função para obter produtos
    if (callId) { getProducts.call($('#id_call')) }
  });

  if ($('[name="user_call"]').length){
    $(document).ready(function() {
      getProducts.call($('#id_call'))
    })
  }

});        