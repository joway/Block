function sidebarCatalog() {
    var catalog = $('#catalog');
    if (catalog.css('display') == 'none') {
        catalog.fadeIn();
    } else {
        catalog.fadeOut();
    }
}
