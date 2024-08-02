$(function() {
  var getProducts = function() {
    var callId = $(this).val();
    if (callId) {
      var productSelects = $('.product-select select');

      productSelects.each(function() {
        var currentSelect = $(this);
        var selectId = currentSelect.attr('id');
        var selectedOption = currentSelect.find('option:selected');
        currentSelect.data(selectId + '-selected-option', selectedOption);
      });

      $.ajax({
        url: '/get_products/',
        type: 'GET',
        data: {'call_id': callId},
        success: function(data) {
          productSelects.each(function() {
            var currentSelect = $(this);
            currentSelect.empty();

            currentSelect.prepend($('<option>', {
              value: '',
              text: '---------',
              selected: true
            }));

            $.each(data.products, function(index, product) {
              currentSelect.append($('<option>', {
                value: product.id,
                text: product.text,
              }));
            });

            var selectId = currentSelect.attr('id');
            if (currentSelect.data(selectId + '-selected-option')) {
              var selectedOption = currentSelect.data(selectId + '-selected-option');
              if (selectedOption) {
                currentSelect.val(selectedOption.val());
              }
            }
          });
        }
      });
    }
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

          if (data.calls.length === 0) {
            currentSelect.append($('<option>', {
              value: '',
              text: 'Sem chamadas',
              selected: true
            }));
          }
          else {
            currentSelect.prepend($('<option>', {
              value: '',
              text: '---------',
              selected: true
            }));
          }

          $.each(data.calls, function(index, call) {
            currentSelect.append($('<option>', {
              value: call.id,
              text: call.text,
            }));
          });
        });

        if (data.calls.length > 0) {
          getProducts.call($('#id_call'));
      }
      }
    });
  };

  var getBalance = function() {
    var productSelect = $(this);
    var productRow = productSelect.closest('.inlineform');
    var productBalance = productRow.find('.product-balance');
    var productId = productSelect.val();

    if (!productId) {
      productBalance.text('. . .');
      return;
    }

    $.ajax({
      url: '/get_balance/',
      type: 'GET',
      data: {'product_id': productId},
      success: function(data) {
        productBalance.text(data.balance)
      }
    });
  };

  $('#id_institution').on('change', getCalls);
  $('#id_call').on('change', getProducts)
  $(document).on('change', 'select[id$="call_product"]', getBalance);

  $('.add-row').click(function() {
    var callId = $('#id_call').val();
    if (callId) {
      getProducts.call($('#id_call'))
    }
  });

  if ($('[name="user_call"]').length){
    $(document).ready(function() {
      getProducts.call($('[name="user_call"]'))
    })
  }

});