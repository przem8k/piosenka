$(document).ready(function(){
    $('.site-search input').typeahead([
        {
            name: 'songs',
            prefetch: '/index/songs',
            header: '<p class="dataset-header">Piosenki</p>'
        },
        {
            name: 'artists',
            prefetch: '/index/artists',
            header: '<p class="dataset-header">Artyści</p>'
        }
    ]).on('typeahead:selected', function($e, data) {
          window.location = data.url;
    });
});
