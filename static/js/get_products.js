'use strict';

$(function() {
  const getProducts = function() {
    const callId = $(this).val();
    const dataUrl = $(this).attr('data-url');

    if (!dataUrl) return;

    if (callId) {
      const productSelects = $('.product-select select');

      productSelects.each(function() {
        const currentSelect = $(this);
        const selectId = currentSelect.attr('id');
        const selectedOption = currentSelect.find('option:selected');
        currentSelect.data(`${selectId}-selected-option`, selectedOption);
      });

      $.ajax({
        url: dataUrl,
        type: 'GET',
        data: {'call_id': callId},
        success: function(data) {
          productSelects.each(function() {
            const currentSelect = $(this);
            currentSelect.empty().prepend($('<option>', {
              value: '',
              text: '---------',
              selected: true
            }));

            $.each(data.products, (index, product) => {
              currentSelect.append($('<option>', {
                value: product.id,
                text: product.text,
                'data-price': product.price
              }));
            });

            const selectId = currentSelect.attr('id');
            const selectedOption = currentSelect.data(`${selectId}-selected-option`);
            if (selectedOption) {
              currentSelect.val(selectedOption.val());
            }
          });

          getOrderTotal();
        }
      });
    }
  };

  const getCalls = function() {
    const institutionId = $('#id_institution').val();
    const dataUrl = $(this).attr('data-url');
    const callSelects = $('#id_call');

    if (!dataUrl) return;

    $.ajax({
      url: dataUrl,
      type: 'GET',
      data: {'institution_id': institutionId},
      success: function(data) {
        callSelects.empty();

        callSelects.append($('<option>', {
          value: '',
          text: data.calls.length === 0 ? 'Sem chamadas' : '---------',
          selected: true
        }));

        $.each(data.calls, (index, call) => {
          callSelects.append($('<option>', {
            value: call.id,
            text: call.text,
          }));
        });

        if (data.calls.length > 0) {
          getProducts.call($('#id_call'));
        }
      }
    });
  };

  const getBalance = function() {
    const dataUrl = $(this).attr('data-url-balance');
    const productId = $(this).val();

    const productRow = $(this).closest('.inlineform');
    const productBalance = productRow.find('.product-balance');

    if (!dataUrl) return;

    $.ajax({
      url: dataUrl,
      type: 'GET',
      data: {'product_id': productId},
      success: (data) => productBalance.text(data.balance || '. . .')
    });
  };

  const getUnit = function() {
    const productId = $(this).val();
    const dataUrl = $(this).attr('data-url-unit');

    const productRow = $(this).closest('.inlineform');
    const productTd = productRow.find('.inline-balance');
    const productUnit = productTd.find('.product-unit');

    if (!dataUrl) return;

    $.ajax({
      url: dataUrl,
      type: 'GET',
      data: {'product_id': productId},
      success: (data) => productUnit.text(data.unit || '. . .')
    });
  };

  const getOrderTotal = function() {
    let orderTotal = 0;

    $('tr.inlineform').each(function() {
      const row = $(this);
      const select = row.find('select[id$="call_product"]');
      const quantityInput = row.find('input[id$="ordered_quantity"]');
      const unitPriceCell = row.find('.unit-price');
      const productTotalCell = row.find('.product-total');

      const price = parseFloat(select.find('option:selected').data('price')) || 0;
      const quantity = parseFloat(quantityInput.val()) || 0;
      const productTotal = price * quantity;

      unitPriceCell.text(price.toFixed(2).replace('.', ','));
      unitPriceCell.attr('data-value', price.toFixed(2));

      productTotalCell.text(productTotal.toFixed(2).replace('.', ','));
      productTotalCell.attr('data-value', productTotal.toFixed(2));

      orderTotal += productTotal;
    });

    $('#order-total').text(orderTotal.toFixed(2).replace('.', ','));
  };

  $('#id_institution').on('change', getCalls);
  $('#id_call').on('change', getProducts);

  $(document).on('change', 'select[id$="call_product"]', function() {
    getBalance.call(this);
    getOrderTotal();
  });

  $(document).on('input change', 'input[id$="ordered_quantity"]', getOrderTotal);

  if ($('.product-unit').length){
    $(document).on('change', 'select[id$="product"]', getUnit);
  }

  $('.add-row').click(() => {
    const callId = $('#id_call').val();
    if (callId) getProducts.call($('#id_call'));
  });

  if ($('[name="user_call"]').length) {
    getProducts.call($('[name="user_call"]'));
  }

  getOrderTotal();
});
