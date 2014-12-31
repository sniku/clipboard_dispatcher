
add_extra_row = function(){
    var rows = $('#actions_table tbody tr').length;
    var $action_row = $("#action_row").clone();
    var row_number = rows;
    $action_row.attr('id', 'id'+row_number);
    $action_row.appendTo("#actions_table tbody");
}

load_row = function(row){
    var rows = $('#actions_table tbody tr').length;
    var $action_row = $("#action_row").clone();
    var row_number = rows;
    $action_row.attr('id', 'id'+row_number);
    $action_row.find('input[name=name]').attr("value", row.name);
    $action_row.find('input[name=type]').attr("value", row.type);
    $action_row.find('input[name=target]').attr("value", row.target);

    $action_row.appendTo("#actions_table tbody");
}


load_options = function(callback){
    chrome.storage.sync.get("actions", function(obj) {
      console.log(obj);
        for(i in obj.actions){
            r = obj.actions[i];
            load_row(r);
        }
        callback();
    });
};
save_options = function(){
    var actions = [];
    $('#actions_table tbody tr').each(function(i){
        var vals = {
            name:    $(this).find('input[name=name]').val(),
            type:    $(this).find('input[name=type]').val(),
            target:  $(this).find('input[name=target]').val()
        };

        // TODO: add some validation here
        if(vals.name != "")
            actions.push(vals);
    });
        console.log(actions);
        chrome.storage.sync.set({'actions': actions }, function() {
        // Notify that we saved.
        console.log('Settings saved');
    });


};
$(document).ready(function(){
    load_options(function(){
        add_extra_row();
    });

    $("#save_button").click(function(e){
        save_options();
        if($('#actions_table tbody tr').last().find('input[name=name]').val()!=""){
            add_extra_row();
        }
        e.preventDefault();
    });

    $('#actions_table').on('click', 'img.delete', function() {
            console.log(this);
            $(this).parent().parent().remove();
    });

});
