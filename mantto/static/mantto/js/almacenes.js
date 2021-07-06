function getCards(data,container)
{
    jQuery.each(data.results, function(i, producto) {
        container.append(getNode(producto));
    });
}

function getNode(data)
{
    var out = '<div class="card product-card">';
    if (data.producto.foto) out += '<img class="card-img-top" src="'+ data.producto.foto +'">';
    out += '<div class="card-body">';
    out += '<h5 class="card-title">'+data.producto.nombre+'</h5>';
    out += '<p class="card-text">ID: '+data.producto.id+'<br>Presentación: '+data.producto.presentacion+'<br> Costo: $'+data.producto.costo+ ' <br> \
    Gym: '+ data.gym.nombre +' <br> Existencias: '+ data.existencias +'</p>';
    out += '</div></div>';
    return out;
}

function getAlmacenes(url)
{
    var container = $('#almacenContainer');
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
    url = $('#almacenContainer').attr('data-source');
    nombre = $( "#nombreInput" ).val();

    if(nombre)
    {
        url = addParameters(url,'nombre',nombre);
    }
    getAlmacenes(url);
}

$( document ).ready(function() {
    addFilters();
});