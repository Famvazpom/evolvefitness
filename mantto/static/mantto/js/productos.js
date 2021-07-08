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
    
    if(data.activo=='Activo')
    {
        eliminar = '<a onclick="openModal(\''+data.eliminar+'\')" class="btn btn-danger m-1"> Desactivar </a>';
        console.log('a');
    }
    else{
        eliminar = '<a onclick="openModal(\''+data.eliminar+'\')" class="btn btn-info m-1"> Activar </a>';
        console.log('b');
    }
    
    return [
        data.id,
        foto,
        data.nombre.nombre,
        data.marca,
        data.presentacion,
        data.costo,
        data.activo,
        detalles,
        eliminar
    ]
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