//  garante que o código dentro da função seja executado somente após o carregamento completo do DOM
$(document).ready(function() {
    // pego a classe, e informo o evento: 'show.bs...'
    $('.dropdown').on('show.bs.dropdown', function() {
        var $dropdownMenu = $(this).find('.dropdown-menu'); // seleciono o menu dentro do dropdown

        $('body').append($dropdownMenu.detach()); // separo o drop do container da table-responsive com detach() "ao mesmo tempo" q o body o adiciona
        
        var $dropdown = $(this);   //armazeno o que acionou o evento
        var offSet = $dropdown.offset();  //obtem a posiçao do drop

        // largura e altura do drop
        var dropdownWidth = $dropdownMenu.outerWidth();
        var dropdownHeight = $dropdownMenu.outerHeight();
        
        // ajusta a posição para garantir que o dropdown não saia da tela enquanto arrasta a table
        var align_left = offSet.left - ($dropdownMenu.outerWidth() / 2) + ($dropdown.outerWidth() / 2);

        //css
        $dropdownMenu.css({
            'display': 'block',
            'top': offSet.top + $dropdown.outerHeight(),
            'left': align_left
        });
    });

    //ocultar o drop e retomar a posiçao original
    $('.dropdown').on('hide.bs.dropdown', function(e) {
        $(e.target).append($('.dropdown-menu', this).detach());
        $('.dropdown-menu', this).hide();
    });
});