function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function getProduct(item) {
    out = "<button class='col-auto btn p-0' onclick='agregarAlCarrito(\""+item.id+"\")'>";
    out+='<div class="card product-venta-card">';
    out+='<div class="card-body p-1" style=\'background-image: url("'+item.producto.foto+'");\' >';
    out+="<span class='product-info'>";
    out+='<h5 class="card-title">'+item.producto.nombre.nombre+'</h5>';
    out+='<p class="card-text p-0">';
    out+=''+item.producto.marca+'<br>'+item.producto.presentacion+'';
    out+='<br> <strong>'+item.precio+'</strong>  <br> Existencias: '+item.existencias+'</p></span></div></div></button>';
    return out;
}

function addRow(id)
{
    url = $('#productoMuestra').attr('data-src');
    url = addParameters(url,'almacen',id);
    
    $.ajax({
        url: url,
        type: "GET", 
        dataType: "json",

        success: function(data) {
            item = data[0];
            $('#carritoTable tbody').append('<tr id="'+item.id+'">\
            <td>'+item.producto.nombre.nombre+'</td>\
            <td class="text-center">'+item.existencias+'</td>\
            <td class="text-center"><input id="'+item.id+'_precio" disabled class="form-control" value="'+item.precio.replace('$','')+'" type="number"></td>\
            <td class="text-center"><input min=0 onchange="ChangeValues(\''+item.id+'\')" id="'+item.id+'_cant" class="form-control" value=1 type="number"></td>\
            <td class="text-center"><input id="'+item.id+'_importe" disabled step=.1 class="form-control" value="'+item.precio.replace('$','')+'" type="number"></td>\
            <td><button class="btn btn-danger" onclick="deleteRow(\''+item.id+'\')">X</button></td></tr>');
            UpdateTotal();
        }
    });
}

function ChangeValues(item)
{
    var precio = document.getElementById(item+'_precio');
    var cantidad = document.getElementById(item+'_cant');
    var importe = document.getElementById(item+'_importe');
    var total = 0;
    if(cantidad.value != '')
    {
        importe.value = parseFloat(cantidad.value * precio.value);
    }
    UpdateTotal();
}

function deleteRow(id) {
    document.getElementById(id).remove();
    UpdateTotal();
}

function UpdateTotal()
{
    var total = 0;
    rows = $('#carritoTable').find('tbody').find('tr');

    for (var i = 0; i < rows.length; i++) {
        var id = rows[i].id;
        var precio = document.getElementById(id+'_precio').value;
        var cant = document.getElementById(id+'_cant').value;
        total += parseInt(cant) * parseFloat(precio);
    }
    if(document.getElementById('descuento').value == '')
    {
        document.getElementById('descuento').value = 0;

    }
    if(total > document.getElementById('descuento').value)
    {
        total -= parseFloat(document.getElementById('descuento').value);
    }
    document.getElementById('total').value = parseFloat(total).toFixed(2);
}


function agregarAlCarrito(id)
{
    obj = document.getElementById(id+'_cant');
    if(obj)
    {
        obj.value = parseInt(obj.value)+1;
        ChangeValues(id);
    }
    else
    {
        addRow(id);
    }
    
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
            createProducts(data,container);
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

function Cobrar()
{
    datad= [];
    data = {};
    var rows = $('#carritoTable').find('tbody').find('tr');
    jQuery.each(rows, function(i, row) {
        var cant = document.getElementById(row.id+'_cant').value;
        var item = {
            'id': row.id,
            'cantidad': cant,
        };
        datad.push(item);
        row.remove()
    });
    data['productos'] = JSON.stringify(datad);
    data['descuento'] = document.getElementById('descuento').value;
    
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    $.ajax({
        data: data,
        type: 'POST',
        success:function(json){
            alert('Venta Exitosa');
            getData();
            UpdateTotal();
        },
        error: function(data){
            errors = 'ERROR\n';
            jQuery.each(data.responseJSON, function(i, val) {
                jQuery.each(val, function(i, obj) {
                    errors += obj.message + '\n';
                });
            });
            alert(errors);
            UpdateTotal();
        }
    })  
}


$( document ).ready(function() {
    getData();
});