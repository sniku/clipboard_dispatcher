var edit = document.getElementById('edit');
edit.addEventListener('doCopy', function(e) {
  console.log('Content script caught custom event.');
  edit.focus();
  document.execCommand('copy');
  console.log('Content script executed copy command.');
});
