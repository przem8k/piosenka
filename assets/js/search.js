$(document).ready(function(){
    var songs = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: '/index/songs',
    });
    songs.initialize();

    var artists = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: '/index/artists',
    });
    artists.initialize();

    var selected = false;

    $('.search input').typeahead({
        hint: false,
        highlight: false,
    }, {
        name: 'songs',
        source: songs.ttAdapter(),
        templates: {
            header: '<p class="dataset-header">Piosenki</p>',
        }
    }, {
        name: 'artists',
        source: artists.ttAdapter(),
        templates: {
            header: '<p class="dataset-header">Artyści</p>',
        },
    }).on('typeahead:selected', function($e, data) {
      window.location = data.url;
      selected = true;
    }).on( "keydown", function(event) {
      if(event.which == 13 && !selected) {
        window.location = '/szukaj/?q=' + encodeURIComponent(this.value);
      }
    });
});
