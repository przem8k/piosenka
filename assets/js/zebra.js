document.addEventListener("DOMContentLoaded", function() {
    if (document.querySelectorAll(".lyrics table").length === 0) return;

    function updateZebra() {
        //check the height of an unwrapped lyrics line
        const firstCell = document.querySelector(".lyrics table td");
        const lineHeight = parseInt(window.getComputedStyle(firstCell).lineHeight) || 20;

        //check if any line in lyrics is higher, i.e. wrapped
        const chordsAbove = document.querySelector(".lyrics").classList.contains("chords-above");
        const isWrapped = Array.from(document.querySelectorAll(".lyrics table tr")).some(function(tr) {
            if (chordsAbove) {
                //rows with chords above are taller, so count lines of the text itself
                const bottoms = new Set();
                tr.querySelector("td").childNodes.forEach(function(node) {
                    if (node.nodeType != Node.TEXT_NODE) return;
                    const range = document.createRange();
                    range.selectNodeContents(node);
                    Array.from(range.getClientRects()).forEach(function(rect) {
                        bottoms.add(Math.round(rect.bottom));
                    });
                });
                return bottoms.size > 1;
            }
            return tr.getBoundingClientRect().height > lineHeight * 1.5;
        });

        //add/remove zebra class for the whole song
        document.querySelector(".lyrics").classList.toggle("zebra", isWrapped);
    }

    updateZebra();
    window.addEventListener("resize", updateZebra);
    //fired by song.js when the layout may change (chords view, transposition, font)
    window.addEventListener("chordsviewchange", updateZebra);
});
