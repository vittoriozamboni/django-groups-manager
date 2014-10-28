function multiple_form_validation_errors(tot_elements, form_model, errors_list, form_prefix) {
    var error_string = '';
    var errors = [];
    for (var s=0; s<tot_elements; s++) {
        l_errors = errors_list[s];
        var l_number = s + 1;
        ks = _.keys(l_errors);
        if (ks.length > 0) {
            for (var k=0; k<ks.length; k++) {
                var field_name = '';
                if (ks[k] != '__all__') {
                    field_name = "in field <strong>" + ks[k] + "</strong>";
                    var error_string = 'Error in ' + form_model + ' <strong>' + (l_number) + '</strong> ' + field_name + ': ' + l_errors[ks[k]];
                    errors.push(error_string);
                    $("[name='" + form_prefix + "-" + s + "-" + ks[k] + "']").addClass('field-error');
                } else {
                    for (var i=0; i<l_errors['__all__'].length; i++) {
                        var error_string = 'Validation error in form <strong>' + (l_number) + '</strong>: ' + l_errors['__all__'][i];
                        errors.push(error_string);
                    }                    
                }
                
            }  
        }
    }
    errors_string = '<ul><li>' + errors.join('</li><li>') + '</li></ul>';
    return {'list': errors, 'string': errors_string};
}
