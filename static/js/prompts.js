function prompt_warning(msg, timeout) {
  var $toastContent = $('<span class="red-text">' + msg + '</span>');
  Materialize.toast($toastContent, timeout);
}
function prompt_success(msg, timeout) {
  var $toastContent = $('<span>' + msg + '</span>');
  Materialize.toast($toastContent, timeout);
}
