/*
 * Requirements:
 *  - textarea: a textarea with an ID, that become hidden
 *  - a prefix for the table 
 */
function dictionaryField_create(field_id) {
    prefix = field_id + '_dictionaryField_table';
    $('#' + field_id).after(
        '<table class="table table-striped table-condensed dictionaryfield dictionaryfield-table" id="' + prefix + '" data-field_id="' + field_id + '">' +
        '<thead>' +
            '<th>Key</th><th>Value</th><th></th>' +
        '</thead>' +
        '<tbody></tbody>' +
        '</table>'
    );
    $('#' + prefix).delegate('i.dictionaryfield-remove', 'click', function(){
        dictionaryField_remove($(this).attr('data-couple_id'));
    });
    $('#' + field_id + '_dictionaryField_table').delegate('.dictionaryfield', 'blur', function(){
        dictionaryField_update($(this).attr('data-prefix'));
    });
    preload = $.parseJSON($("#" + field_id).val());
    $.each(preload, function(key, value) {
        t = dictionaryField_add_item_string(prefix, key.toString(), value.toString());
        $('#' + prefix + ' tr:last').after(t);    
    });
    t = dictionaryField_add_item_string(prefix);
    $('#' + prefix + ' tr:last').after(t);    
    add_span = 
        '<span class="dictionaryfield dictionaryfield-add-couple" ' +
            'style="cursor: pointer" ' +
            'onclick="dictionaryField_add_couple(\'' + prefix + '\');">' + 
                '<i class="icon-plus"></i> Add value' +
        '</span>';
    $('#' + prefix).after(add_span);
    $('#' + field_id).hide();
}


function dictionaryField_update(prefix) {
    field_id = $("#" + prefix).attr('data-field_id');
    dictionary = {};
    $("tr[data-prefix='" + prefix + "']").each(function(){
        key = $("#key_" + prefix + "_" + $(this).attr('data-uuid')).val();
        console.log(key);
        if (key != '') {
            value = $("#value_" + prefix + "_" + $(this).attr('data-uuid')).val();
            dictionary[key] = value;
        } 
    });
    $("#" + field_id).val($.toJSON(dictionary));
}

function dictionaryField_add_item_string(prefix, dict_key, dict_val) {
    if (!dict_key) dict_key = '';
    if (!dict_val) dict_val = '';

    uuid = UUID.generate();
    couple_id = prefix + "_" + uuid;
    var t = "<tr id='couple_" + couple_id + "' " +
                "data-uuid='" + uuid + "' data-prefix='" + prefix + "'>" +
               "<td>" +
                  "<input type='text' value='" + dict_key + "'" +
                       "class='dictionaryfield dictionaryfield-key " + prefix + "-key' " +
                       "data-prefix='" + prefix + "'" +
                       "name='key_" + prefix + "_" + uuid + "' " +
                       "id='key_" + prefix + "_" + uuid + "' /> " +
                "</td>" +
               "<td>" +
                  "<input type='text' value='" + dict_val + "'" +
                       "class='dictionaryfield dictionaryfield-value " + prefix + "-value' " +
                       "data-prefix='" + prefix + "'" +
                       "name='value_" + prefix + "_" + uuid + "' " +
                       "id='value_" + prefix + "_" + uuid + "' /> " +
                "</td>" +
               "<td style='width: 20px;'>" +
                  "<i class='icon-minus-sign dictionaryfield-remove' style='cursor:pointer;' " +
                    "data-couple_id='" + couple_id + "'></i>" +
                "</td>" +
             "</tr>";
    return t;
}


function dictionaryField_remove(couple_id) {
    $row = $('#couple_' + couple_id);
    prefix = $row.attr('data-prefix');
    $row.remove();
    dictionaryField_update(prefix);
}

function dictionaryField_add_couple(prefix) {
    t = dictionaryField_add_item_string(prefix);
    $('#' + prefix + ' tr:last').after(t);
}

