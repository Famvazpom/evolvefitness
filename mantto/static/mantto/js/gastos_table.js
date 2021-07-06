$(document).ready( function () {
    var table = $("#gastosTable").DataTable(
        {
            "searching": false
        }
    );
    addFilters();
} );

function createGastoRows(container,data)
{
    end = [];
    for(var i = 0; i<data.length;i++ )
    {
       end.push(getRow(data[i]));
    }
   container.rows.add(end).draw();
}

function pagadoText(pagado)
{
    return pagado? "Si": "No"; 
}
function getRow(data)
{
    cont = $('#gastosTable').attr('admin');
     if (cont)
     {
        out = [
            data.fecha,
            data.gym,
            data.proveedor,
            data.descripcion,   
            data.importe,
            data.forma_pago,
            data.pago,
            pagadoText(data.pagado),
            data.detalles,
            data.reportes,
            data.eliminar
        ];
     }
     else
     {
        out = [
            data.fecha,
            data.gym,
            data.proveedor,
            data.descripcion,   
            data.importe,
            data.forma_pago,
            data.pago,
            pagadoText(data.pagado),
            data.detalles,
            data.reportes,
        ];
     }
    
    return out;
}

function getGastos(url)
{
    var container = $('#gastosTable').DataTable();
    $.ajax({
        url: url,
        type: "GET", 
        dataType: "json",

        success: function(data) {
            container.clear();
            createGastoRows(container,data);
        },
        error:function(data) {
        }
    });
}


function addFilters()
{
    url = $('#gastosTable').attr('data-source');
    getGastos(url);
}
