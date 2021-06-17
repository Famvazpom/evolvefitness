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