/*
 * Requires:
 *  - jquery
 *  - bootstrap popover
 * 
 * This utilities are built on top of django_utilities models and templates.
 * 
 * Author: Vittorio Zamboni
 * 
 */

function django_helper_forms_ajax_post_form_errors(form_id, errors) {
    /*
     * This function highlights in red the labels of fields that are not
     * valid after post submission of a form.
     * It also shows the icon near the form field and set the error text
     * as popover content.
     * 
     * Template must have field and icon like:
     * <label id='address_label' for='address'>Address</label>
     * <input name='address' />
     * <i class='icon-remove-sign' id='address_errors' style='display:none'>
     * 
     */
    $(".form-error-icon", $("#" + form_id)).hide();
    $(".form-label", $("#" + form_id)).removeClass('color-red');
    $.each(errors, function(field_name, error) {
        $("#" + field_name + '_errors').show();
        $("#" + field_name + '_label').addClass('color-red');
        $("#" + field_name + '_errors').popover({
            content: error[0],
            placement: 'left',
            trigger: 'hover'
        })
    });
}
