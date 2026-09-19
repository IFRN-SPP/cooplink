'use strict';

$(function() {
  let productsRequest;
  let callsRequest;

  const clearProducts = function() {
    $('.product-select select').empty().append($('<option>', {
      value: '', text: '---------'
    }));
    $('.product-balance').empty();
    getOrderTotal();
  };

  const getProducts = function() {
    const callId = $('#id_call').val();
    const dataUrl = $('#id_call').attr('data-url');

    if (productsRequest) productsRequest.abort();

    if (!callId || !dataUrl) {
      clearProducts();
      return;
    }

    productsRequest = $.ajax({
      url: dataUrl,
      type: 'GET',
      data: {'call_id': callId},
      success: function(data) {
        if ($('#id_call').val() !== callId) return;

        $('.product-select select').each(function() {
          const currentSelect = $(this);
          const selectedValue = currentSelect.val();
          currentSelect.empty().append($('<option>', {
            value: '', text: '---------'
          }));

          $.each(data.products, (index, product) => {
            currentSelect.append($('<option>', {
              value: product.id,
              text: product.text,
              'data-price': product.price
            }));
          });

          currentSelect.val(selectedValue || '');
          if (!currentSelect.val()) currentSelect.val('');
          getBalance.call(this);
        });

        getOrderTotal();
      },
      error: function(xhr, status) {
        if (status !== 'abort') $('#order-total').text('Indisponível');
      }
    });
  };

  const getCalls = function() {
    const institutionId = $('#id_institution').val();
    const dataUrl = $(this).attr('data-url');
    const callSelects = $('#id_call');

    if (!dataUrl) return;

    if (callsRequest) callsRequest.abort();
    callSelects.empty().append($('<option>', {value: '', text: '---------'}));
    callSelects.trigger('change');
    if (!institutionId) return;

    callsRequest = $.ajax({
      url: dataUrl,
      type: 'GET',
      data: {'institution_id': institutionId},
      success: function(data) {
        if ($('#id_institution').val() !== institutionId) return;
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
      }
    });
  };

  const getBalance = function() {
    const dataUrl = $(this).attr('data-url-balance');
    const productId = $(this).val();

    const productRow = $(this).closest('.inlineform');
    const productBalance = productRow.find('.product-balance');
    const productSelect = $(this);

    productBalance.empty();
    if (!productId || !dataUrl) return;

    $.ajax({
      url: dataUrl,
      type: 'GET',
      data: {'product_id': productId},
      success: function(data) {
        if (productSelect.val() === productId) {
          productBalance.text(data.balance || '. . .');
        }
      }
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

  // Preço e quantidade têm duas casas: 10,50 vira 1050; 1,25 vira 125.
  // Usar inteiros evita diferenças de centavos nas multiplicações e somas.
  const decimalToInteger = function(value) {
    const scaled = Math.round(Number(String(value || 0).replace(',', '.')) * 100);
    return Number.isFinite(scaled) ? BigInt(scaled) : 0n;
  };

  // O produto tem quatro casas decimais. Na exibição, reduzimos para duas.
  // Empates vão para o centavo par, como no servidor: 0,005 -> 0,00; 0,015 -> 0,02.
  const formatMoney = function(value) {
    const negative = value < 0n;
    const absolute = negative ? -value : value;
    let cents = absolute / 100n;
    const remainder = absolute % 100n;
    const roundUpTie = remainder === 50n && cents % 2n !== 0n;
    if (remainder > 50n || roundUpTie) cents++;
    return `${negative && cents ? '-' : ''}${cents / 100n},${String(cents % 100n).padStart(2, '0')}`;
  };

  const getOrderTotal = function() {
    let orderTotal = 0n;
    let missingPrice = false;

    $('tr.inlineform').each(function() {
      const row = $(this);
      const deleteInput = row.find('input[id$="-DELETE"]');
      const isDeleted = deleteInput.is(':checkbox')
        ? deleteInput.is(':checked') : Boolean(deleteInput.val());
      if (isDeleted) return;

      const select = row.find('select[id$="call_product"]');
      const quantityInput = row.find('input[id$="ordered_quantity"]');
      const unitPriceCell = row.find('.unit-price');
      const productTotalCell = row.find('.product-total');

      const priceValue = select.find('option:selected').attr('data-price');
      if (select.val() && priceValue === undefined) {
        unitPriceCell.text('Indisponível');
        productTotalCell.text('Indisponível');
        missingPrice = true;
        return;
      }
      const price = decimalToInteger(priceValue);
      const quantity = decimalToInteger(quantityInput.val());
      const productTotal = price * quantity;

      unitPriceCell.text(formatMoney(price * 100n));
      productTotalCell.text(formatMoney(productTotal));

      orderTotal += productTotal;
    });

    $('#order-total').text(missingPrice ? 'Indisponível' : formatMoney(orderTotal));
  };

  $('#id_institution').on('change', getCalls);
  $('#id_call').on('change', function() {
    $('input[id$="ordered_quantity"]').val('');
    clearProducts();
    getProducts();
  });

  $(document).on('change', 'select[id$="call_product"]', function() {
    getBalance.call(this);
    getOrderTotal();
  });

  $(document).on('input change', 'input[id$="ordered_quantity"]', getOrderTotal);

  if ($('.product-unit').length){
    $(document).on('change', 'select[id$="product"]', getUnit);
  }

  $(document).on('change', 'input[id$="-DELETE"]', getOrderTotal);

  // A mesma configuração atende à criação pelo cliente, pela equipe e à edição.
  const orderFormset = $('[data-order-formset-prefix]');
  if (orderFormset.length) {
    orderFormset.find('.inlineform').formset({
      prefix: orderFormset.attr('data-order-formset-prefix'),
      addText: '<button type="button" class="btn btn-success btn-gap"><i class="bi bi-plus-circle"></i>ADICIONAR PRODUTO</button>',
      deleteText: '<button type="button" class="btn btn-danger btn-sm ms-2"><i class="bi bi-trash3-fill"></i></button>',
      added: getProducts,
      removed: getOrderTotal,
    });
  }

  if ($('#id_call').length) {
    getProducts();
  }

  getOrderTotal();
});
