$(document).ready(function(){
    var songs = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: '/index/songs.json',
        limit: 10,
    });
    songs.initialize();

    // Prefer exact matches, so that "Ja" returns the song "Ja" before "Był Jazz"
    // See https://github.com/twitter/typeahead.js/issues/817 .
    var orig_get = songs.get;
    songs.get = function (query, cb) {
        return orig_get.apply( songs, [query, function (suggestions) {
            if ( !suggestions ) return cb(suggestions);
            suggestions.forEach(function(s) {
                s.exact_match = query.toLowerCase() === s.name.toLowerCase()? 1: 0; 
            });
            suggestions.sort(function(a, b) {
                return a.exact_match > b.exact_match? -1 : a.exact_match < b.exact_match? 1 : 0
            });
            cb(suggestions);
        } ]);
    };

    var artists = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: '/index/artists.json',
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
