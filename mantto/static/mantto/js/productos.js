function getCards(data,container)
{
    jQuery.each(data, function(i, producto) {
        container.append(getNode(producto));
    });
}

function getNode(data)
{
    var out = '<div class="card product-card">';
    if (data.foto) out += '<img class="card-img-top" src="'+ data.foto +'">';
    out += '<div class="card-body">';
    out += '<h5 class="card-title">'+data.nombre+'</h5>';
    out += '<p class="card-text">Presentación: '+data.presentacion+'<br> Costo: $'+data.costo+ ' <br> Marca: '+data.marca+' <br> Proveedor: '+ data.proveedor +'</p>';
    out += '<a onclick="openModal(\''+data.detalles+'\')" class="btn btn-primary m-1">Detalles</a>';
    out += '<a onclick="openModal(\''+data.eliminar+'\')" class="btn btn-danger m-1">Eliminar</a>';
    out += '</div></div>';
    return out;
}

function getProductos(url)
{
    var container = $('#productoContainer');
    $.ajax({
        url: url,
        type: "GET", 
        dataType: "json",

        success: function(data) {
            container.empty();
            getCards(data,container);
        }
    });
}

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



function addFilters()
{
    url = $('#productoContainer').attr('data-source');
    nombre = $( "#nombreInput" ).val();

    if(nombre)
    {
        url = addParameters(url,'nombre',nombre);
    }
    getProductos(url);
}

$( document ).ready(function() {
    addFilters();
});