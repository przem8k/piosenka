$(document).ready(function(){
    $('.site-search .typeahead').typeahead([
        {
            name: 'songs',
            prefetch: '/index/songs',
            header: '<h3>Piosenki</h3>'
        },
        {
            name: 'artists',
            prefetch: '/index/artists',
            header: '<h3>Artyści</h3>'
        }]);
});
