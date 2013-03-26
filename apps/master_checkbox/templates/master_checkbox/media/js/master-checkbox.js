//TODO synchronize masters of a same group

//a checkbox that controls multiple checkboxes
//give it class master-checkbox and an id
//and for the checkbox it controls give them slave-of attribute equal to the mater's id
//each slave can have multiple masters, space separated

//input parameters
var master_checkbox_group_attr = '{{ master_checkbox_group_attr }}';
var slave_checkbox_group_attr = '{{ slave_checkbox_group_attr }}';

$(document).ready(function() 
    {
        $('body :checkbox['+master_checkbox_group_attr+']').click(function() {
            $('body :checkbox['+slave_checkbox_group_attr+'~="'+$(this).attr(master_checkbox_group_attr)+'"]').attr('checked', this.checked );
        });     
    }
); 
