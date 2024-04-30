$(function(){
    var loadForm = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function(data){
                $("#modal-form .modal-content").html(data.html_form);
                $("#modal-form").modal("show");
            }
        });
    };
    
    var saveForm = function(){
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function(data){
                if(data.form_is_valid){
                    if(data.success_url){
                        loadList(data.success_url)
                    }
                    $("#modal-form").modal("hide");
                    if(data.message){
                        console.log(data.message)
                        if(data.message_class) {
                            addMessage(data.message, data.message_class)
                        } else {
                            addMessage(data.message)
                        }
                    }
                }
                else if (data.protected_error){
                    $("#modal-form").modal("hide");
                    addMessage(data.message, data.message_class)
                }
                else{
                    $("#modal-form .modal-content").html(data.html_form)
                }
            }
        });
        return false
    };

    var loadList = function(url) {
        $.ajax({
            type: "get",
            url: url,
            dataType: "json",
            success: function(data) {
                $('#partial-table tbody').html(data.html_list);
                if (data.html_pagination) {
                    $('#partial-page').html(data.html_pagination);
                }
                if ($('#filter-form').length > 0){
                    $('#filter-form')[0].reset()
                }
            }
        });
    };

    var filter = function(){
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function(data){
                console.log(data)
                $('#partial-table tbody').html(data.html_list);
                if (data.html_pagination){
                    $('#partial-page').html(data.html_pagination);
                }
            }
        });
        return false
    }

    var paginatation = function(){
        var url = $(this).attr("data-url");
        $.ajax({
            url: url,
            type: 'get',
            dataType: 'json',
            success: function(data){
                $("#partial-table tbody").html(data.html_list);
                if(data.html_pagination){
                    $("#partial-page").html(data.html_pagination);
                }
            }
        });
        return false
    };
 
    function addMessage(text, messageClass){
        var alert = $('<div class="alert ' + messageClass + ' alert-dismissible fade show fw-bold" role="alert">' + text + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');

        if ($('#message').length) {$('#message').append(alert)}
    }

    // CREATE
    $(".js-create").click(loadForm);
    $("#modal-form").on("submit", ".js-create-form", saveForm);

    // UPDATE
    $("#partial-table").on("click", ".js-update", loadForm);
    $("#modal-form").on("submit", ".js-update-form", saveForm);

    // DELETE
    $("#partial-table").on("click", ".js-delete", loadForm);
    $("#modal-form").on("submit", ".js-delete-form", saveForm); 
    
    // PAGINATION
    $("#partial-page").on("click", ".js-link", paginatation);

    // FILTER
    $("#filter-form").on("input", filter);
    $("#filter-form").on("submit", filter);

    // BTN RESET FILTER 
    $('.btn-reset').on("click", function() {
        loadList('?')
    });

});