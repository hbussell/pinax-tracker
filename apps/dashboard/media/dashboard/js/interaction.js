
$('#task_name').val('Add task').addClass('label_input');

$('#task_name').focus(function (){
    if($(this).val()=='Add task'){
        $(this).val('').removeClass('label_input');
    }
});

$('#project_name').val('Add project').addClass('label_input');
$('#project_name').focus(function (){
    if($(this).val()=='Add project'){
        $(this).val('').removeClass('label_input');
    }
});

