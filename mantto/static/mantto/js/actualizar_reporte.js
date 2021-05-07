$(document).on('submit','#modal_form',function(event)
{
    var action = $('#modal_form').attr('action');
    var ob =$('button[type=submit]');
    ob.prop('disabled',true);
    var formdata = $('#modal_form').serialize();
    event.preventDefault();
    
    $.ajax({
        data: formdata,
        url: action,
        processData: false,  // tell jQuery not to process the data

        type: $('#modal_form').attr('method'),
        success:function(json){
            location.reload();
        },
        error: function(data){
            alert('ERROR');
            jQuery.each(data.responseJSON, function(i, val) {
                //console.log(i,val);
            });
            ob.prop('disabled',false);
        }
    })  
});