
function openModal(url)
{
    $('#modalForm').load(url,function(){
        $(this).modal({
            show: true,
            backdrop: 'static', 
            keyboard: false
        });
    });
}