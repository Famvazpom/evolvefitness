
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
    var out = '<div class="card p-1">';
    out += '<div class="card-body text-center">';
    out += '<h5 class="card-title">'+data.gym.nombre+'<br> ID : '+ data.equipo.id +'</h5>';
    out += '<h6 class="card-subtitle mb-2 text-muted '+ data.estado.css_class +' ">'+data.estado.nombre+'</h6>';
    out += '<p class="card-text text-justify">'+ data.falla +'</p>';
    if(data.costo)
    {
        out += '<p class="card-text"> Costo: $'+ data.costo +'</p>';
    }
    
    out += '<a onclick="openModal(\''+data.url+'\')" class="card-link btn btn-info ">Detalles</a>';
    if(data.foto)
    {   
        out += '<a onclick="openModal(\''+data.foto_url+'\')" class="card-link btn btn-info ">Ver Fotos</a>';
    }
    else{
        out += '<a class="card-link btn btn-info ">Sin Fotos</a>';
    }
    
    if(data.revisado)
    {
        out += '<br><small class="text-muted"> Revisado </small>';
    }
    else{
        out += '<br><small class="text-muted"> Sin revisar </small>';
    }
    out += '</div>';
    out +='<div class="card-footer">'
    out += '<small class="text-muted"> Ultima Modificación: '+ data.ultima_modificacion +'</small>'
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
    console.log(url);
    changeActiveClass(st_pk);
    getReportCards(url);
}

$(document).ready( function () {
    getReportCards($('#cardContainer').attr('data-source'));
} );