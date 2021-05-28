
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
    var out = '<div class="card m-3">';
    out += '<div class="card-body text-center">';
    out += '<h5 class="card-title">'+data.gym.nombre+'</h5>';
    out += '<h6 class="card-subtitle mb-2 text-muted '+ data.estado.css_class +' ">'+data.estado.nombre+'</h6>';
    out += '<p class="card-text">'+ data.falla +'</p>';
    out += '<a onclick="openModal(\''+data.url+'\')" class="card-link btn btn-info ">Detalles</a>';
    out += '</div>';
    out +='<div class="card-footer">'
    out += '<small class="text-muted"> Ultima Modificación: '+ data.ultima_modificacion +'</small>'
    out += '</div>';
    out += '</div>';
    return out;
}

function addPagination(data)
{
    var out = '<nav aria-label="Page navigation example">';
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
            console.log(data);
            createReportCards(container,pag,data);
        },
        error:function(data) {
            console.log(data); 
        }
    });
}


$(document).ready( function () {
    getReportCards($('#cardContainer').attr('data-source'));
} );