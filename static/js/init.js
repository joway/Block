$('#side-nav-menu').sideNav({'edge': 'left'});


$(document).ready(function () {
  $('.modal').modal({
      dismissible: true, // Modal can be dismissed by clicking outside of the modal
      opacity: .5, // Opacity of modal background
      in_duration: 300, // Transition in duration
      out_duration: 200, // Transition out duration
      starting_top: '4%', // Starting top style attribute
      ending_top: '10%', // Ending top style attribute
      ready: function (modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
        var id = trigger[0].dataset.id;
        var redirect = trigger[0].dataset.redirect;
        if (id) {
          app.modal.delete.id = id;
        }
        if (redirect) {
          app.modal.delete.redirect = redirect;
        }
      },
      complete: function () {
      } // Callback for Modal close
    }
  );

});
