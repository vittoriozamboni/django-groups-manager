function show_single_form(div_form_id) {
    bootstrapModal("#" + div_form_id, {
        content_as_id: true,
        width: 560,
        min_height: 450,
        //return_id: "#" + div_form_id + '_container',
        disable_cancel: true,
        buttons: {
            'set': {
                'callback': function(){
                    single_form_to_table(div_form_id);
                },
                'button_class': ['btn-info']
            }
        }
    });
}

function show_multiple_form(multiple_form_id) {
    added = false;
    $("#" + multiple_form_id + "_selected_elements").empty();
    $("input[type=checkbox][id^='sample_checked_']").each(function(){
        if ($(this).is(":checked")) {
            added = true;
            element_id = $(this).val();
            $("#" + multiple_form_id + "_selected_elements").append(
                  '<div>' + $("#" + form_element_name + "_" + element_id + "_name").html() + '</div>' 
            );
        }
    });
    if (!added) {
        $("#" + multiple_form_id + "_selected_elements").append(
              '<div>To edit multiple elements at the same time, select elements from the table by clicking on the checkbox in the first column.</div>' 
        );
    }
    bootstrapModal("#" + multiple_form_id, {
        content_as_id: true,
        width: 560,
        min_height: 450,
        //return_id: "#" + multiple_form_id + '_container',
        buttons: {
            'set': {
                'callback': function(){
                    multiple_form_to_single_form(multiple_form_id);
                },
                'button_class': ['btn-success']
            }
        }
    });
}

function single_form_to_table(div_form_id) {
    element_id = $("#" + div_form_id).attr('data-element-id');
    form_prefix = $("#" + div_form_id).attr('data-form-prefix');
    for (fi=0; fi<form_element_table_fields.length; fi++) {
        field = form_element_table_fields[fi];
        id_field = "#id_" + form_prefix + '-' + field;
        if ($(id_field)[0].nodeName == 'INPUT') {
            value = $(id_field).val();
        } else
        if ($(id_field)[0].nodeName == 'SELECT') {
            value = $(id_field + ' option:selected').text();
        }
        $("#" + form_element_name + '_' + element_id + '_' + field).html(value);
    }
}

function multiple_form_to_single_form(multiple_form_id) {
    value = $("#" + multiple_form_id + "_value").val();
    console.log("#" + multiple_form_id + "_value", value);
    field_name = $("#" + multiple_form_id).attr('data-element-name');
    console.log("field_name", field_name);
    multiple_apply_to = $("input[id='" + multiple_form_id + "_apply_to']:checked").val();
    console.log("multiple_apply_to", multiple_apply_to);
    $("input[type=checkbox][id^='" + form_element_name + "_checked_']").each(function(){
        if ($(this).is(":checked") || multiple_apply_to == 'all') {
            element_id = $(this).val();
            form_id = form_element_name + "_form_" + element_id;
            prefix = $("#" + form_id).attr('data-form-prefix');
            console.log("apply to", form_id);
            console.log("id", "#id_" + prefix + '-' + field_name);
            $("#id_" + prefix + '-' + field_name).attr("value", value);
        }
    });
    $("input[type=checkbox][id^='" + form_element_name + "_checked_']").each(function(){
        if ($(this).is(":checked") || multiple_apply_to == 'all') {
            element_id = $(this).val();
            form_id = form_element_name + "_form_" + element_id;
            single_form_to_table(form_id);
        }
    });
}
