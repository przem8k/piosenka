$(document).ready(function() {
    if ($(".lyrics table").length === 0) return;

    function updateZebra() {
        //check the height of an unwrapped lyrics line
        const lineHeight = parseInt($(".lyrics table td").first().css("line-height")) || 20;

        //check if any line in lyrics is higher, i.e. wrapped
        const isWrapped = $(".lyrics table tr").toArray().some(function(tr) {
            return $(tr).height() > lineHeight * 1.5;
        });

        //add/remove zebra class for the whole song
        $(".lyrics").toggleClass("zebra", isWrapped);
    }

    updateZebra();
    $(window).on("resize", updateZebra);
});
