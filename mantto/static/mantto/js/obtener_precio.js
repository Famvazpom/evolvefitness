function addParameters(url,prefix,parameter)
{
    if(url.includes('?'))
    {
        url += '&'+prefix+'='+parameter;
    }
    else
    {
        url += '?'+prefix+'='+parameter;
    }
    return url;
}


function obtenerPrecio()
{
    gym = $('select[name="gym"] option').filter(':selected').val();
    producto = $('select[name="producto"] option').filter(':selected').val();
    url = $('#modal_form').attr('data-src');
    if(gym && producto)
    {
        url = addParameters(url,'gym',gym);
        url = addParameters(url,'producto',producto);
        getPrecio(url);
    }
}

function getPrecio(url)
{
    
    $.ajax({
        url: url,
        type: "GET", 
        dataType: "json",

        success: function(data) {
           $('input[name="precio"]').val(data.precio);
        }
    });
}

$( 'select[name="gym"]').change(function() {
    obtenerPrecio();
});
$( 'select[name="producto"]').change(function() {
    obtenerPrecio();
});