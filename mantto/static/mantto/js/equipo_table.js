$(document).ready( function () {
    var table = $("#equipoTable").DataTable(
        {
            "searching": false
        }
    );
} );

function createEquipoRows(container,data)
{
    end = [];
    for(var i = 0; i<data.results.length;i++ )
    {
       end.push(getRow(data.results[i]));
    }
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


function getRow(data)
{
    if(data.modificar)
    {
        out = [
            data.id,
            data.nombre,
            data.marca,
            data.gym.nombre,   
            data.modificar,
            data.reportar
        ];
    }
    else{
        out = [
            data.id,
            data.nombre,
            data.marca,
            data.gym.nombre,   
            data.reportar
        ];
    }
    
    return out;
}

function getEquipos(url)
{
    var container = $('#equipoTable').DataTable();
    $.ajax({
        url: url,
        type: "GET", 
        dataType: "json",

        success: function(data) {
            container.clear();
            createEquipoRows(container,data);
        },
        error:function(data) {
        }
    });
}


function addFilters()
{
    url = $('#equipoTable').attr('data-source');
    idmaquina = $( "#idmaquinaInput" ).val();
    maquina = $( "#maquinaInput" ).val();
    marca = $( "#marcaInput" ).val();
    gym = $( "#gymSelect option:selected" ).val();
    if(idmaquina)
    {
        url = addParameters(url,'id-maquina',idmaquina);
    }
    if(maquina)
    {
        url = addParameters(url,'maquina',maquina);
    }
    if(maquina)
    {
        url = addParameters(url,'marca',marca);
    }
    if(gym)
    {
        url = addParameters(url,'gym',gym);
    }
    getEquipos(url);
}
