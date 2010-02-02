
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

$('#taskbar .option-expander').click(function (){
    $('#taskbar .extra-options').toggleClass('show-options');
    $('#taskbar .option-expander').toggleClass('hide-expander');
});

$('#filter-task-link').click(function (){
        console.log('clicked filter');
    $('#task-filter').toggleClass('show-options');
});
