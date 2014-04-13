var GadgetStateEnum = {
    NORMAL: 0,
    REPEATED: 1,
    NONE: 2
};

var gadgetState = GadgetStateEnum.NORMAL;
var transposition = 0;

function applyState() {
    $(".chords-trigger").removeClass("btn-primary");
    $(".chords-trigger").addClass("btn-default");
    if (gadgetState == GadgetStateEnum.NORMAL) {
        $(".chord-section").show();
        $(".extra-chords").hide();
        $(".chords-normal-trigger").addClass("btn-primary").removeClass("btn-default");
    } else if (gadgetState == GadgetStateEnum.REPEATED) {
        $(".chord-section").show();
        $(".extra-chords").show();
        $(".chords-repeated-trigger").addClass("btn-primary").removeClass("btn-default");
    } else if (gadgetState == GadgetStateEnum.NONE) {
        $(".chord-section").hide();
        $(".chords-none-trigger").addClass("btn-primary").removeClass("btn-default");
    }
}

function transpose() {
    $.ajax({
        url: transpositionUrls[transposition],
    }).done(function(data) {
        $("#lyrics").replaceWith(data['lyrics']);
        applyState();
    });
}

$(document).ready(function(){
    $(".chords-normal-trigger").click(function() {
        gadgetState = GadgetStateEnum.NORMAL;
        applyState();
    });
    $(".chords-repeated-trigger").click(function() {
        gadgetState = GadgetStateEnum.REPEATED;
        applyState();
    });
    $(".chords-none-trigger").click(function() {
        gadgetState = GadgetStateEnum.NONE;
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
