document.addEventListener("DOMContentLoaded", function() {
    if (document.querySelectorAll(".lyrics table").length === 0) return;

    function updateZebra() {
        //check the height of an unwrapped lyrics line
        const firstCell = document.querySelector(".lyrics table td");
        const lineHeight = parseInt(window.getComputedStyle(firstCell).lineHeight) || 20;

        //check if any line in lyrics is higher, i.e. wrapped
        const isWrapped = Array.from(document.querySelectorAll(".lyrics table tr")).some(function(tr) {
            return tr.getBoundingClientRect().height > lineHeight * 1.5;
        });

        //add/remove zebra class for the whole song
        document.querySelector(".lyrics").classList.toggle("zebra", isWrapped);
    }

    updateZebra();
    window.addEventListener("resize", updateZebra);
});
