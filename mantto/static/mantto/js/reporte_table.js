
function createReportCards(container,pag,data)
{   
    for(var i = 0; i<data.results.length;i++ )
    {
        container.append(getNode(data.results[i]));
    }
    pag.append(addPagination(data));
}

function getNode(data)
{
    var out = '<div class="card p-2">';
        out += '<div class="card-body table-responsive text-center">';
            out += '<table class="table table-sm table-dark">';
            out += '<tr><td>'+data.gym.nombre +'</td> <td>ID: '+ data.equipo.id +'</td><td>'+ data.equipo.nombre +'</td><td class=" card-subtitle mb-2 text-muted  '+ data.estado.css_class +'">'+ data.estado.nombre +'</td></tr>';
            out += '<tr><td>'+data.asignado +'</td>';
            if(data.costo)
            {
                out += '<td> $'+ data.costo +'</td>';
            } 
            else{
                out += '<td></td>';
            }
            if(data.tipopago)
            {
                out += '<td>'+ data.tipopago.nombre +'</td><td></td></tr>';
            } 
            else{
                out += '<td></td><td></td></tr>';
            }
            out += '<tr><td>'+ data.fecha +'</td><td class"text-justify" colspan=3>'+ data.falla +'</td></tr>';
            if(data.mensajes)
            {
                jQuery.each(data.mensajes, function(i, msg) {
                    console.log(msg);
                    out += '<tr><td>'+ msg.fecha +'</td><td class"text-justify" colspan=3>'+ msg.mensaje +'</td></tr>';
                });
            }
            out += '<tr><td><a onclick="openModal(\''+data.url+'\')" class="card-link btn btn-info ">Detalles</a></td></tr>';

            out += '</table>';
        out += '</div>';
    out += '</div>';
    return out;
}

function addPagination(data)
{
    var out = '<nav>';
        out += '<ul class="pagination justify-content-center">';
        if (data.previous)
        {
            out += '<li class="page-item"><a class="page-link" onclick="getReportCards(\''+data.previous+'\')">Anterior</a></li>';
        }
        out += '<li class="page-item active"><a class="page-link">'+data.pageNumber+'</a></li>';
        if(data.next)
        {
            out += '<li class="page-item"><a class="page-link" onclick="getReportCards(\''+data.next+'\')">Siguiente</a></li>';
        }
        out += '</ul>';
        out += '</nav>';
    return out;
}

function getReportCards(url)
{
    var container = $('#cardContainer');
    var pag = $('#cardPagination');
    $.ajax({
        url: url,
        type: "GET", 
        dataType: "json",

        success: function(data) {
            container.empty();
            pag.empty();
            createReportCards(container,pag,data);
        },
        error:function(data) {
        }
    });
}

function changeActiveClass(st_pk)
{   
    $('#reportFilterNav .active').removeClass('active');
    if(st_pk)
    {
        $("[st-pk="+st_pk+"]").addClass('active');
    }
    else{
        $('#generalTab').addClass('active');
    }

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

function addFilters(st_pk)
{
    url = $('#cardContainer').attr('data-source');
    maquina = $( "#maquinaInput" ).val();
    gym = $( "#gymSelect option:selected" ).val();
    asignado = $( "#asignadoSelect option:selected" ).val();
    revisado = $( "#revisadoSelect option:selected" ).val();
    if(maquina)
    {
        url = addParameters(url,'maquina',maquina);
    }
    if(gym)
    {
        url = addParameters(url,'gym',gym);
    }
    if(asignado)
    {
        url = addParameters(url,'asignado',asignado);
    }
    if(st_pk)
    {
        url = addParameters(url,'status',st_pk);
    }
    if(revisado)
    {
        url = addParameters(url,'revisado',revisado);
    }
    changeActiveClass(st_pk);
    getReportCards(url);
}

$(document).ready( function () {
    getReportCards($('#cardContainer').attr('data-source'));
} );