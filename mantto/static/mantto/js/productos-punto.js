function getProduct(item) {
    out = "<button class='btn p-0' onclick='alert(\"data\")'>";
    out+='<div class="card product-venta-card">';
    out+='<div class="card-body p-1" style=\'background-image: url("'+item.producto.foto+'");\' >';
    out+="<span class='product-info'>";
    out+='<h5 class="card-title">'+item.producto.nombre+'</h5>';
    out+='<p class="card-text">';
    out+=''+item.producto.presentacion+'<br>'+item.producto.marca+'';
    out+='<br> <strong>'+item.precio+'</strong>  <br></p></span></div></div></button>';
    return out;
}


function createProducts(data,container)
{
    jQuery.each(data, function(i, producto) {
        container.append(getProduct(producto));
    });
}

function getData(){
    container = $('#productoMuestra');
    url = container.attr('data-src');
    url = addParameters(url,'gym',container.attr('data-gym'));
    $.ajax({
        url: url,
        type: "GET", 
        dataType: "json",

        success: function(data) {
            container.empty();
            createProducts(data,container)
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


$( document ).ready(function() {
    getData();
});