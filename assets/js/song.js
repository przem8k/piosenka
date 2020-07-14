var GadgetStateEnum = {
    CHORDS_ON: 0,
    CHORDS_OFF: 2
};

var gadgetState = GadgetStateEnum.CHORDS_ON;
var transposition = 0;

function enableTransposition() {
    $(".trans-up-trigger").prop('disabled', false);
    $(".trans-home-trigger").prop('disabled', false);
    $(".trans-down-trigger").prop('disabled', false);
}

function disableTransposition() {
    $(".trans-up-trigger").prop('disabled', true);
    $(".trans-home-trigger").prop('disabled', true);
    $(".trans-down-trigger").prop('disabled', true);
}

function applyState() {
    $(".chords-trigger").removeClass("btn-primary");
    $(".chords-trigger").addClass("btn-default");
    if (gadgetState == GadgetStateEnum.CHORDS_ON) {
        $(".chord-section").show();
        $(".chords-normal-trigger").addClass("btn-primary").removeClass("btn-default");
        enableTransposition();
    } else if (gadgetState == GadgetStateEnum.CHORDS_OFF) {
        $(".chord-section").hide();
        $(".chords-none-trigger").addClass("btn-primary").removeClass("btn-default");
        disableTransposition();
    }
}

function transpose() {
    $.ajax({
        url: transpositionUrls[transposition],
    }).done(function(data) {
        $(".lyrics-content").replaceWith(data['lyrics']);
        applyState();
    });
}

$(document).ready(function(){
    $(".chords-normal-trigger").click(function() {
        gadgetState = GadgetStateEnum.CHORDS_ON;
        applyState();
    });
    $(".chords-none-trigger").click(function() {
        gadgetState = GadgetStateEnum.CHORDS_OFF;
        applyState();
    });

    $(".trans-up-trigger").click(function() {
        transposition = (transposition + 1) % 12;
        transpose();
    });
    $(".trans-home-trigger").click(function() {
        transposition = 0;
        transpose();
    });
    $(".trans-down-trigger").click(function() {
        transposition = (transposition + 11) % 12;
        transpose();
    });
});
