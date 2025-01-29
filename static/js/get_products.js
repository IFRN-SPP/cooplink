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
              }));
            });

            const selectId = currentSelect.attr('id');
            const selectedOption = currentSelect.data(`${selectId}-selected-option`);
            if (selectedOption) {
              currentSelect.val(selectedOption.val());
            }
          });
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

  $('#id_institution').on('change', getCalls);
  $('#id_call').on('change', getProducts);
  $(document).on('change', 'select[id$="call_product"]', getBalance);

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
});
