$(document).ready( function () {
    $('#equipoTable thead tr').clone(true).appendTo( '#equipoTable thead' );
    $('#equipoTable thead tr:eq(1) th').each( function (i) {
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="Buscar por '+title+'" />' );
 
        $( 'input', this ).on( 'keyup change', function () {
            if ( table.column(i).search() !== this.value ) {
                table
                    .column(i)
                    .search( this.value )
                    .draw();
            }
        } );
    } );
    var table = $("#equipoTable").DataTable();
} );