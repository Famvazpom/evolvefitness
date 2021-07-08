function getCards(data,container)
{
    jQuery.each(data, function(i, producto) {
        container.append(getNode(producto));
    });
}

function getRow(data) {

    if(data.foto)
    {
        foto = '<img class="product-photo" src="'+data.foto+'">';
    }
    else{
        foto = null;
    }
    detalles = '<a onclick="openModal(\''+data.detalles+'\')" class="btn btn-primary m-1"> Detalles </a>';
    eliminar = '<a onclick="openModal(\''+data.eliminar+'\')" class="btn btn-danger m-1"> Eliminar </a>';
    return [
        data.id,
        foto,
        data.nombre,
        data.marca,
        data.presentacion,
        data.costo,
        detalles,
        eliminar
    ]
}

function getNode(data)
{
    var out = '<div class="card product-card">';
    if (data.foto) out += '<img class="card-img-top" src="'+ data.foto +'">';
    out += '<div class="card-body">';
    out += '<h5 class="card-title">'+data.nombre+'</h5>';
    out += '<p class="card-text">Presentación: '+data.presentacion+'<br> Costo: '+data.costo+ ' <br> Marca: '+data.marca+' <br> Proveedor: '+ data.proveedor +'</p>';
    out += '<a onclick="openModal(\''+data.detalles+'\')" class="btn btn-primary m-1">Detalles</a>';
    out += '<a onclick="openModal(\''+data.eliminar+'\')" class="btn btn-danger m-1">Eliminar</a>';
    out += '</div></div>';
    return out;
}


function getProductosT(url)
{
    var container = $('#productosTable').DataTable();
    $.ajax({
        url: url,
        type: "GET", 
        dataType: "json",

        success: function(data) {
            container.clear();
            getRows(data,container);
        }
    });
}


function getRows(data,container)
{
    end = [];
    jQuery.each(data, function(i, producto) {
        end.push(getRow(data[i]));
    });
    container.rows.add(end).draw();
    console.log('in',end);
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
    url = $('#productosTable').attr('data-source');
    console.log(url);
    nombre = $( "#nombreInput" ).val();
    marca = $( "#marcaInput" ).val();
    presentacion = $( "#presentacionInput" ).val();

    if(nombre)
    {
        url = addParameters(url,'nombre',nombre);
    }
    if(marca)
    {
        url = addParameters(url,'marca',marca);
    }
    if(presentacion)
    {
        url = addParameters(url,'presentacion',presentacion);
    }
    getProductosT(url);
}


$( document ).ready(function() {
    var table = $("#productosTable").DataTable({
        "searching": false
    });
    addFilters();
});