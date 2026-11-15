var GadgetStateEnum = {
    CHORDS_ON: 0,
    CHORDS_ABOVE: 1,
    CHORDS_OFF: 2
};

let gadgetState = GadgetStateEnum.CHORDS_ON;
let transposition = 0;

function $$(selector) {
    return document.querySelectorAll(selector);
}

function setDisabled(selector, disabled) {
    $$(selector).forEach(el => { el.disabled = disabled; });
}

function setActive(selector, active) {
    $$(selector).forEach(el => {
        el.classList.toggle("btn-primary", active);
        el.classList.toggle("btn-secondary", !active);
    });
}

function setVisible(selector, visible, displayWhenVisible) {
    const value = visible ? (displayWhenVisible || "") : "none";
    $$(selector).forEach(el => { el.style.display = value; });
}

function onClick(selector, handler) {
    $$(selector).forEach(el => el.addEventListener("click", handler));
}

function enableTransposition() {
    setDisabled(".trans-up-trigger, .trans-home-trigger, .trans-down-trigger", false);
}

function disableTransposition() {
    setDisabled(".trans-up-trigger, .trans-home-trigger, .trans-down-trigger", true);
}

const ABOVE_STORAGE_KEY = "chordsAbove";

function rememberChordsView(above) {
    try {
        localStorage.setItem(ABOVE_STORAGE_KEY, above ? "1" : "0");
    } catch (e) {}
}

// fill the .ch marks with chords from the chord column, in order (lyrics.py checks the count),
// the tail mark gets the rest
function fillChordsAbove() {
    $$(".lyrics tr").forEach(tr => {
        const marks = tr.querySelectorAll(".ch");
        const column = tr.querySelector(`.chord-section .chords-t${transposition}`);
        if (!marks.length || !column) return;
        const chords = column.textContent.trim().split(/\s+/);
        let i = 0;
        marks.forEach(mark => {
            if (mark.classList.contains("tail")) {
                mark.dataset.c = chords.slice(i).join(" ");
            } else {
                const n = Number(mark.dataset.n || 1);
                mark.dataset.c = chords.slice(i, i + n).join(" ");
                i += n;
            }
        });
    });
}

const chordCanvas = document.createElement("canvas").getContext("2d");

// chords above take no space in the line: move a chord right if it overlaps the previous one,
// and move a chord sticking out of the lyrics back left
function fixChordsAbove() {
    const marks = $$(".lyrics .ch");
    marks.forEach(mark => {
        mark.style.marginLeft = "";
        mark.style.removeProperty("--shift");
    });
    if (gadgetState != GadgetStateEnum.CHORDS_ABOVE) return;
    let prevRight = -Infinity, prevBottom = null;
    marks.forEach(mark => {
        let rect = mark.getBoundingClientRect();
        if (mark.classList.contains("tail")) {
            // the tail takes real width, move it after the last chord if they overlap
            const sameLine = prevBottom !== null && rect.top < prevBottom;
            if (sameLine && rect.left < prevRight) {
                const margin = parseFloat(getComputedStyle(mark).marginLeft);
                mark.style.marginLeft = (margin + prevRight - rect.left) + "px";
            }
            prevBottom = null;
            return;
        }
        if (Math.round(rect.bottom) != prevBottom) prevRight = -Infinity; // next visual line
        if (rect.left < prevRight) {
            mark.style.marginLeft = (prevRight - rect.left) + "px";
            rect = mark.getBoundingClientRect();
        }
        const style = getComputedStyle(mark, "::before");
        chordCanvas.font = `${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
        const width = chordCanvas.measureText(mark.dataset.c).width;
        const outside = rect.left + width - mark.closest("td").getBoundingClientRect().right;
        if (outside > 0) mark.style.setProperty("--shift", -outside + "px");
        prevRight = rect.left + width + parseFloat(style.fontSize) * 0.4;
        prevBottom = Math.round(rect.bottom);
    });
}

function updateChordsAbove() {
    if (gadgetState == GadgetStateEnum.CHORDS_ABOVE) fillChordsAbove();
    fixChordsAbove();
}

function applyState() {
    setActive(".chords-trigger", false);
    $$(".lyrics").forEach(el => {
        el.classList.toggle("chords-above", gadgetState == GadgetStateEnum.CHORDS_ABOVE);
    });
    if (gadgetState == GadgetStateEnum.CHORDS_ON) {
        setVisible(".chord-section", true);
        setActive(".chords-normal-trigger", true);
        enableTransposition();
    } else if (gadgetState == GadgetStateEnum.CHORDS_ABOVE) {
        setVisible(".chord-section", false);
        setActive(".chords-above-trigger", true);
        enableTransposition();
    } else if (gadgetState == GadgetStateEnum.CHORDS_OFF) {
        setVisible(".chord-section", false);
        setActive(".chords-none-trigger", true);
        disableTransposition();
    }
    updateChordsAbove();
    // the row layout may have changed (zebra.js)
    window.dispatchEvent(new Event("chordsviewchange"));
}

function transpose() {
    for (let i = 0; i <= 11; i++) {
        setVisible(`.chords-t${i}`, false);
    }
    // .chords-tN spans have `display: none` in CSS by default, so showing
    // them needs an explicit visible value rather than "".
    setVisible(`.chords-t${transposition}`, true, "inline");
    applyState();
}

document.addEventListener("DOMContentLoaded", function() {
    onClick(".chords-normal-trigger", () => {
        gadgetState = GadgetStateEnum.CHORDS_ON;
        rememberChordsView(false);
        applyState();
    });
    onClick(".chords-above-trigger", () => {
        gadgetState = GadgetStateEnum.CHORDS_ABOVE;
        rememberChordsView(true);
        applyState();
    });
    onClick(".chords-none-trigger", () => {
        gadgetState = GadgetStateEnum.CHORDS_OFF;
        applyState();
    });

    onClick(".trans-up-trigger", () => {
        transposition = (transposition + 1) % 12;
        transpose();
    });
    onClick(".trans-home-trigger", () => {
        transposition = 0;
        transpose();
    });
    onClick(".trans-down-trigger", () => {
        transposition = (transposition + 11) % 12;
        transpose();
    });

    // the button exists only for songs with ^ marks
    if ($$(".chords-above-trigger").length) {
        let remembered = null;
        try {
            remembered = localStorage.getItem(ABOVE_STORAGE_KEY);
        } catch (e) {}
        if (remembered == "1") {
            gadgetState = GadgetStateEnum.CHORDS_ABOVE;
            applyState();
        }

        window.addEventListener("resize", fixChordsAbove);
        // chord positions depend on the web font
        document.fonts.ready.then(applyState);
    }
});
