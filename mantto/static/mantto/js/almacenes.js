function getCards(data,container)
{
    end = [];
    jQuery.each(data, function(i, producto) {
        end.push(getRow(data[i]));
    });
    container.rows.add(end).draw();
}

function getRow(data)
{
    out = [
        data.producto.id,
        data.gym.nombre,
        data.producto.nombre.nombre,
        data.producto.marca,
        data.producto.presentacion,   
        data.producto.costo,
        data.precio,
        data.existencias,
    ];
    return out;
}

function getAlmacenes(url)
{
    var container = $('#almacenContainer').DataTable();
    $.ajax({
        url: url,
        type: "GET", 
        dataType: "json",

        success: function(data) {
            container.clear();
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
    marca = $( "#marcaInput" ).val();
    presentacion = $( "#presentacionInput" ).val();
    gym = $( "#gymSelect" ).val();


    if(gym)
    {
        url = addParameters(url,'gym',gym);
    }
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
    getAlmacenes(url);
}

$( document ).ready(function() {
    var table = $("#almacenContainer").DataTable(
        {
            "searching": false
        }
    );
    addFilters();
});



