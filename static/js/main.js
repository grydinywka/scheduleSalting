function modifyButtons() {
    var inp = 'input.btn';

    $(inp).wrapAll( '<div class="form-group" />' );
    $(inp).wrapAll( '<div class="controls col-sm-6" id="buttons" />' );
    $('<label class="col-sm-2 control-label"></label>').insertBefore($('#buttons'));
}

function initDateFields() {
	var inp = 'input.dateinput';

//    $('div.input-group').addClass('date');
	$(inp).datetimepicker({
        format: 'YYYY-MM-DD',
        locale: 'uk'
    }).on('dp.hide', function(event){
        $(this).blur();
    });
}

$(document).ready(function(){
    modifyButtons();
    initDateFields();
});
