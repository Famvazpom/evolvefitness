function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function deleteFoto(url,pk)
{
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    $.ajax({
        url: url,
        processData: false,
        contentType: false,

        type: 'POST',
        success:function(json){
            alert('Eliminacion Correcta');
            $('#'+pk).remove();
        },
        error: function(data){
            errors = 'ERROR\n';
            jQuery.each(data.responseJSON, function(i, val) {
                jQuery.each(val, function(i, obj) {
                    errors += obj.message + '\n';
                });
            });
            alert(errors);
            ob.prop('disabled',false);
        }
    })  
}


$(document).on('submit','#modal_form',function(event)
{
    var action = $('#modal_form').attr('action');
    var ob =$('button[type=submit]');
    ob.prop('disabled',true);
    var formdata = new FormData($("#modal_form")[0]);
    event.preventDefault();

    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    $.ajax({
        data: formdata,
        url: action,
        processData: false,
        contentType: false,

        type: $('#modal_form').attr('method'),
        success:function(json){
            location.reload();
        },
        error: function(data){
            errors = 'ERROR\n';
            jQuery.each(data.responseJSON, function(i, val) {
                jQuery.each(val, function(i, obj) {
                    errors += obj.message + '\n';
                });
            });
            alert(errors);
            ob.prop('disabled',false);
        }
    })  
});