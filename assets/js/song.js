var GadgetStateEnum = {
    CHORDS_ON: 0,
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

function applyState() {
    setActive(".chords-trigger", false);
    if (gadgetState == GadgetStateEnum.CHORDS_ON) {
        setVisible(".chord-section", true);
        setActive(".chords-normal-trigger", true);
        enableTransposition();
    } else if (gadgetState == GadgetStateEnum.CHORDS_OFF) {
        setVisible(".chord-section", false);
        setActive(".chords-none-trigger", true);
        disableTransposition();
    }
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
});
