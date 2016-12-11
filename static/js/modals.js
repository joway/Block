$(document).ready(function () {
  $('#modal-delete').find('.modal-confirm').click(function () {
    $('#modal-delete').modal('close');
    deleteComment(app.modal.delete.id).then(function (response) {
      if (response.ok) {
        if (app.modal.delete.redirect) {
          location.pathname = app.modal.delete.redirect;
        } else {
          location.reload();
        }
        prompt_success('删除成功', 3000);
      } else {
        response.json().then(function (data) {
          prompt_warning(data.detail || '删除失败', 3000);
        });
      }
      app.modal.delete.id = null;
      app.modal.delete.redirect = null;
    });
  });
});


