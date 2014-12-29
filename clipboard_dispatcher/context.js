
function copyTextToClipboard(text) {
  var copyFrom = document.createElement("textarea");
  copyFrom.textContent = text;
  var body = document.getElementsByTagName('body')[0];
  body.appendChild(copyFrom);
  copyFrom.select();
  document.execCommand('copy');
  body.removeChild(copyFrom);
}

// A generic onclick callback function.
function handleContextMenuAction(info, tab, action, context) {

    console.log("info: " + JSON.stringify(info));
    console.log("tab: " + JSON.stringify(tab));

    var payload = {};

    if(context == "image"){
        payload.content = info.srcUrl;
        payload.title = tab.title;
    }
    else if (context == "selection"){
        payload.content = info.selectionText;
        payload.title = tab.title;
    }
    else if (context == "page"){
        payload.content = info.pageUrl + " ("+tab.title+")";
        payload.title = tab.title;
    }

    var dispatch_element = {
        format: 'clipboard_dispatcher',
        version: '0.1',
        payload: payload,
        action: action,
        info: info
    }
    console.log("dispatch_element: " + JSON.stringify(dispatch_element));

    copyTextToClipboard(JSON.stringify(dispatch_element));

}


add_context_menus = function(actions){
    console.log("add_context_menus called");
    chrome.contextMenus.removeAll();
    // Create one test item for each context type.
    var contexts = ["selection", "image", "page"];

    for (var i = 0; i < contexts.length; i++) {
        var context = contexts[i];
        var onclick_callbacks = {};

        for(action_i in actions){
            action = actions[action_i];
            title = action.name + "[" + context + "]";
            console.log(action_i, action, title);

            var onclick = (function(_action, _context){
                return function(info, tab){

                    handleContextMenuAction(info, tab, _action, _context);
    //                console.log("Closures are fucked up");
    //                console.log(_action);
    //                console.log(_context);
                };
            })(action, context);

            var id = chrome.contextMenus.create({"title": title, "contexts":[context],"onclick": onclick});
        }
    }

}

load_settings = function(){
    chrome.storage.sync.get("actions", function(obj) {
        console.log("actions loaded", obj);
        add_context_menus(obj.actions);
    });
}



chrome.storage.onChanged.addListener(function(changes, namespace) {
    load_settings();
});

load_settings();

//
//// Create a parent item and two children.
//var parent = chrome.contextMenus.create({"title": "Test parent item"});
//var child1 = chrome.contextMenus.create(
//  {"title": "Child 1", "parentId": parent, "onclick": genericOnClick});
//var child2 = chrome.contextMenus.create(
//  {"title": "Child 2", "parentId": parent, "onclick": genericOnClick});
//console.log("parent:" + parent + " child1:" + child1 + " child2:" + child2);
//
//
//// Create some radio items.
//function radioOnClick(info, tab) {
//  console.log("radio item " + info.menuItemId +
//              " was clicked (previous checked state was "  +
//              info.wasChecked + ")");
//}
//var radio1 = chrome.contextMenus.create({"title": "Radio 1", "type": "radio",
//                                         "onclick":radioOnClick});
//var radio2 = chrome.contextMenus.create({"title": "Radio 2", "type": "radio",
//                                         "onclick":radioOnClick});
//console.log("radio1:" + radio1 + " radio2:" + radio2);
//
//
//// Create some checkbox items.
//function checkboxOnClick(info, tab) {
//  console.log(JSON.stringify(info));
//  console.log("checkbox item " + info.menuItemId +
//              " was clicked, state is now: " + info.checked +
//              "(previous state was " + info.wasChecked + ")");
//
//}
//var checkbox1 = chrome.contextMenus.create(
//  {"title": "Checkbox1", "type": "checkbox", "onclick":checkboxOnClick});
//var checkbox2 = chrome.contextMenus.create(
//  {"title": "Checkbox2", "type": "checkbox", "onclick":checkboxOnClick});
//console.log("checkbox1:" + checkbox1 + " checkbox2:" + checkbox2);
//
//
//// Intentionally create an invalid item, to show off error checking in the
//// create callback.
//console.log("About to try creating an invalid item - an error about " +
//            "item 999 should show up");
//chrome.contextMenus.create({"title": "Oops", "parentId":999}, function() {
//  if (chrome.extension.lastError) {
//    console.log("Got expected error: " + chrome.extension.lastError.message);
//  }
//});
