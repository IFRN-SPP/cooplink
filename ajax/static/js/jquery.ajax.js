$(function(){
    var loadForm = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function(data){
                $("#ajax-modal .modal-content").html(data.html_form);
                $("#ajax-modal").modal("show");
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
                    $("#ajax-modal").modal("hide");
                    if(data.message){
                        if(data.message_class) {
                            addMessage(data.message, data.message_class)
                        } else {
                            addMessage(data.message)
                        }
                    }
                } else if (data.protected_error){
                    $("#ajax-modal").modal("hide");
                    addMessage(data.message, data.message_class)
                }
                else{
                    $("#ajax-modal .modal-content").html(data.html_form)
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
                $('#ajax-table tbody').html(data.html_list);
                if (data.html_pagination) {
                    $('#ajax-pagination').html(data.html_pagination);
                }
                if ($('#ajax-filter').length > 0){
                    $('#ajax-filter')[0].reset()
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
                $('#ajax-table tbody').html(data.html_list);
                if (data.html_pagination){
                    $('#ajax-pagination').html(data.html_pagination);
                }
            }
        });
        return false
    }

    var pagination = function(){
        var url = $(this).attr("data-url");
        $.ajax({
            url: url,
            type: 'get',
            dataType: 'json',
            success: function(data){
                $("#ajax-table tbody").html(data.html_list);
                if(data.html_pagination){
                    $("#ajax-pagination").html(data.html_pagination);
                }
            }
        });
        return false
    };

    function addMessage(text, messageClass){
        var alert = $('<div class="alert ' + messageClass + ' alert-dismissible fade show" role="alert">' + text + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');

        if ($('#ajax-message').length) {$('#ajax-message').append(alert)}
    }

    // CREATE
    $(".js-create").click(loadForm);
    $("#ajax-modal").on("submit", ".js-create-form", saveForm);

    // UPDATE
    $("#ajax-table").on("click", ".js-update", loadForm);
    $("#ajax-modal").on("submit", ".js-update-form", saveForm);

    // DELETE
    $("#ajax-table").on("click", ".js-delete", loadForm);
    $("#ajax-modal").on("submit", ".js-delete-form", saveForm);

    // PAGINATION
    $("#ajax-pagination").on("click", ".js-link", pagination);

    // FILTER
    $("#ajax-filter").on("input", filter);
    $("#ajax-filter").on("submit", filter);

    // BTN RESET FILTER
    $('.btn-reset').on("click", function() {
        loadList('?')
    });

});