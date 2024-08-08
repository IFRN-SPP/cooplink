$(document).ready(function(){
    if ($('#id_cnpj').length) {
        $('#id_cnpj').mask('00.000.000/0000-00');
    }
    if ($('#id_number').length){
        $('#id_number').mask('000/00');
    }
});