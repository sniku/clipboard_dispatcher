
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
            $action_row.find('input[name=aname]').attr("value", row.aname);
            $action_row.find('input[name=atype]').attr("value", row.atype);
            $action_row.find('input[name=atarget]').attr("value", row.atarget);

            $action_row.appendTo("#actions_table tbody");
        }


        load_options = function(callback){
            chrome.storage.sync.get("rows", function(obj) {
              console.log(obj);
                for(i in obj.rows){
                    r = obj.rows[i];
                    load_row(r);
                }
                callback();
            });
        };
        save_options = function(){
            var rows = [];
            $('#actions_table tbody tr').each(function(i){
                var vals = {
                    aname:    $(this).find('input[name=aname]').val(),
                    atype:    $(this).find('input[name=atype]').val(),
                    atarget:  $(this).find('input[name=atarget]').val()
                }
                rows[i] = vals;

            });
            console.log(rows);
            chrome.storage.sync.set({'rows': rows }, function() {
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
                add_extra_row();
                e.preventDefault();
            });

        });
