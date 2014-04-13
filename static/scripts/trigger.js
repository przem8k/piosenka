$(document).ready(function(){
    $(".chords-none-trigger").click(function() {
        $(".chord-section").hide();
    });
    $(".chords-basic-trigger").click(function() {
        $(".chord-section").show();
        $(".extra-chords").hide();
    });
    $(".chords-all-trigger").click(function() {
        $(".chord-section").show();
        $(".extra-chords").show();
    });
});
