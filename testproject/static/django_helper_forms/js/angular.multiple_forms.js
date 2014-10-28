angular_multiple_form = angular.module('AngularMultipleFormApp', ['ngResource', 'ngCookies', 'ui.bootstrap']);

angular_multiple_form.controller('AngularMultipleFormCtrl', function($scope, $timeout){
    $scope.field_label = '';
    $scope.field = '';
    $scope.return_values = [];
    $scope.select_values = [];
 
    $scope.initialize = function(field_label, field, return_values) {
        $scope.field_label = field_label;
        $scope.field = field;
        if (!return_values) var return_values = []
        $scope.return_values = [];
        for (r=0; r<return_values.length; r++) $scope.return_values.push(return_values[r]);
        if (field['select_values'])
            for (v=0; v<field['select_values'].length; v++) $scope.select_values.push(field['select_values'][v]);
        $scope.$apply();
        $timeout(function(){
            $(".multiple-form-selected-select").selectpicker({'liveSearch': true, 'container': 'body'})
        }, 50);
    }
});



function angular_multiple_form_selected_value($app_scope, object_fields, field_label, field, options) {
    if (!options) var options = {};
    if (!('modal_options' in options)) options['modal_options'] = {};
    if (!('field_text' in options)) options['field_text'] = '';
    if (!('scope_callback' in options)) options['scope_callback'] = null;
    if (!('callback' in options)) options['callback'] = null;
    var modal_options = options['modal_options'];
    var field_text = options['field_text'];
    var scope_callback = options['scope_callback'];
    var callback = options['callback'];
    var return_values = [];
    for (var r=0; r<object_fields.length; r++) {
        if (object_fields[r][2])
            return_values.push(object_fields[r][2]);
        else
            return_values.push(null);
    }
    var text =
    '<div class="row-fluid" id="multiple_form_angular_modal_app" ng-controller="AngularMultipleFormCtrl">' +
    '<div class="span12">' +
        '<div class="bs-callout bs-callout-info">' + 
            '<h4>Change ' + field_label + '</h4>' + 
            '<p>Set ' + field_label + ' for selected elements</p>' +
            '<p>';

    if (field_text != '') {
        text += field_text;
    }
    else if (field['type'] == 'input') {
        text +=
        '<input type="text" class="multiple-form-selected-input-text" ng-model="return_values[0]" />';
    }         
    else if (field['type'] == 'boolean') {
        text +=
        '<input type="checkbox" class="multiple-form-selected-input-text" ng-model="return_values[0]" />';
    }         
    else if (field['type'] == 'date') {
        if (modal_options.width == undefined) modal_options['width'] = 500;
        if (modal_options.height == undefined) modal_options['height'] = 380;
        text +=
        '<datepicker ng-model="return_values[0]" class="well well-sm multiple-form-selected-date"></datepicker>';
    }         
    else if (field['type'] == 'select') {
        text +=
        '<select ng-model="return_values[0]" class="multiple-form-selected-select" ' +
            'ng-options="' + field['options'] + ' in select_values">';
        if (field['options_none'] !== undefined) {
            if (field['options_none'] === true) {
                text += '<option value="">Nothing selected</option>';    
            } else {
                text += '<option value="">' + field['options_none'] + '</option>';
            }
            
        }
        text += '</select>';
    }         
    else if (field['type'] == 'text') {
        if (modal_options.width == undefined) modal_options['width'] = 620;
        if (modal_options.height == undefined) modal_options['height'] = 470;
        text +=
        '<textarea ng-model="return_values[0]" class="multiple-form-selected-text"></textarea>';
    }     
    text += '</p></div></div></div>';
    
    var $scope_form = null;

    modal_options = $.extend({}, {
        title: 'Multiple values for ' + field_label,
        fullscreen: true,
        on_shown: function(){
            angular.bootstrap($("#multiple_form_angular_modal_app")[0], ['AngularMultipleFormApp']);
            $scope_form = angular.element($("#multiple_form_angular_modal_app")).scope();
            $scope_form.initialize(field_label, field, return_values);
        },
        buttons: {
            'set': {
                callback: function() {
                    var processed_element = 0;
                    $(".js-form-element-selector:checked").each(function(){
                        var element_index = $(this).attr('data-index');
                        for (var r=0; r<object_fields.length; r++) {   
                            var ret_value = $scope_form.return_values[r];
                            if (field['type'] == 'text') {
                                try {
                                    ret_value = $scope_form.return_values[r].split('\n')[processed_element]
                                } catch(err) {
                                    ret_value = null;
                                }
                            }
                            if (ret_value !== null)
                                $app_scope[object_fields[r][0]][element_index][object_fields[r][1]] = ret_value;
                            if (field['options_bootstrap_select']) {
                                var sid = field['options_bootstrap_select'].replace('$index', element_index);
                                var value = $('#' + sid + ' option').filter(function () { return $(this).html() == ret_value; }).val();
                                $("#" + sid).selectpicker('val', value);
                            }
                            $app_scope.$apply();
                        }
                        processed_element++;
                    });
                    if (callback) callback($scope_form, $app_scope);
                    if (scope_callback) $app_scope[scope_callback]($scope_form);
                },
                button_class: ['btn-success']
            }
        },
        on_hidden: function(){
            $("#multiple_form_angular_modal_app").remove();
        }
    }, modal_options)
    bootstrapModal(text, modal_options);
}
