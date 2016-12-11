function sidebarCatalog() {
  var catalog = $('#catalog');
  if (catalog.css('display') == 'none') {
    catalog.fadeIn();
  } else {
    catalog.fadeOut();
  }
}

function referredTo(element) {
  var username = element.dataset.username;
  var editor = $('#comment-textarea');
  editor.val(editor.val() + '@' + username + ' ');
  editor.focus();
  return false;
}

function commentUp(element) {
  var thumbUp = $('#thumb-up-' + element.dataset.id);
  if (thumbUp.hasClass('red-text')) {
    thumbUp.addClass('grey-text');
    thumbUp.removeClass('red-text');
  } else {
    thumbUp.addClass('red-text');
    thumbUp.removeClass('grey-text');
  }

  var thumbDown = $('#thumb-down-' + element.dataset.id);
  thumbDown.removeClass('red-text');
  thumbDown.addClass('grey-text');
}

function commentDown(element) {

  var thumbDown = $('#thumb-down-' + element.dataset.id);

  if (thumbDown.hasClass('red-text')) {
    thumbDown.removeClass('red-text');
    thumbDown.addClass('grey-text');
  } else {
    thumbDown.removeClass('grey-text');
    thumbDown.addClass('red-text');
  }

  var thumbUp = $('#thumb-up-' + element.dataset.id);
  thumbUp.removeClass('red-text');
  thumbUp.addClass('grey-text');

}