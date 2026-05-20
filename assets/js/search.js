// Site search autocomplete.
//
// Renders a dropdown of song and artist suggestions under each .search input.
// Songs and artists are fetched once from /index/*.json and matched against
// the input value by tokenizing both sides and prefix-comparing tokens.
// Selecting a suggestion navigates to its URL; submitting without a
// suggestion goes to /szukaj/?q=<value>.

(function () {
    "use strict";

    const SONGS_URL = "/index/songs.json";
    const ARTISTS_URL = "/index/artists.json";
    const SONG_LIMIT = 10;
    const ARTIST_LIMIT = 5;
    const SEARCH_PAGE = "/szukaj/?q=";


    // --- Datasets: fetched once, cached for the rest of the session ---------

    let songs = null;
    let artists = null;
    let loadPromise = null;

    function fetchJson(url) {
        return fetch(url)
            .then((r) => (r.ok ? r.json() : []))
            .catch(() => []);
    }

    function loadIndexes() {
        if (loadPromise) return loadPromise;
        loadPromise = Promise.all([fetchJson(SONGS_URL), fetchJson(ARTISTS_URL)])
            .then(([songsResult, artistsResult]) => {
                songs = songsResult || [];
                artists = artistsResult || [];
            });
        return loadPromise;
    }


    // --- Matching: tokenize query, prefix-match against item tokens ---------

    // Fold Polish diacritics to their ASCII bases so "jalta" finds "Jałta"
    // and "krakow" finds "Kraków" — a common keyboard convenience. NFD
    // splits letters like ć/ó/ą into base + combining mark; ł is a single
    // codepoint (U+0142) so it needs its own replace.
    function foldDiacritics(s) {
        return s.normalize("NFD").replace(/\p{M}+/gu, "").replace(/ł/g, "l").replace(/Ł/g, "L");
    }

    // Split on non-letter / non-digit characters. With the /u flag this is
    // Unicode-aware so any remaining non-ASCII letters stay inside tokens.
    function tokenize(s) {
        return foldDiacritics(s.toLowerCase()).split(/[^\p{L}\p{N}_]+/u).filter(Boolean);
    }

    // Tokenize the item's value with the same regex used for the query so
    // both sides match symmetrically. (gen.py also emits a `tokens` field,
    // but it splits on whitespace and keeps punctuation attached — "(tł."
    // would never prefix-match "tł". Could be removed from gen.py as a
    // follow-up.)
    function itemMatchesAllTokens(item, queryTokens) {
        const itemTokens = tokenize(item.value || item.name || "");
        return queryTokens.every((qt) =>
            itemTokens.some((it) => it.startsWith(qt))
        );
    }

    function searchDataset(query, dataset, limit) {
        const queryTokens = tokenize(query);
        if (queryTokens.length === 0 || !dataset) return [];

        const hits = dataset.filter((item) => itemMatchesAllTokens(item, queryTokens));

        // Float exact name matches to the top so "Ja" returns the song "Ja"
        // before "Był Jazz". Compare folded forms so "jalta" still counts as
        // an exact match for "Jałta".
        const q = foldDiacritics(query.toLowerCase());
        hits.sort((a, b) => {
            const aExact = foldDiacritics(a.name.toLowerCase()) === q ? 0 : 1;
            const bExact = foldDiacritics(b.name.toLowerCase()) === q ? 0 : 1;
            return aExact - bExact;
        });

        return hits.slice(0, limit);
    }


    // --- Rendering: build the dropdown markup -------------------------------

    function escapeHtml(s) {
        const entities = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            "\"": "&quot;",
            "'": "&#39;",
        };
        return String(s).replace(/[&<>"']/g, (c) => entities[c]);
    }

    // Render one (header + items) section, appending each item to `suggestions`
    // so the controller can map a clicked row back to its data object.
    function renderSection(label, hits, baseId, suggestions) {
        if (hits.length === 0) return "";
        let html = `<li class="pzt-suggest-header" aria-hidden="true">${label}</li>`;
        for (const hit of hits) {
            const idx = suggestions.length;
            suggestions.push(hit);
            html += `<li class="pzt-suggest-item" role="option" id="${baseId}-opt-${idx}">${escapeHtml(hit.name)}</li>`;
        }
        return html;
    }


    // --- Controller: per-input dropdown, ARIA, keyboard, selection ---------

    let dropdownIdCounter = 0;

    // One module-level listener handles outside-click for every attached
    // input. Each call to attachAutocomplete registers its own close handler
    // here; the listener iterates them so multiple inputs (collapsed + expanded
    // navbar slots) don't each install their own document-wide listener.
    const outsideClickHandlers = [];
    document.addEventListener("pointerdown", (e) => {
        for (const { wrapper, close } of outsideClickHandlers) {
            if (!wrapper.contains(e.target)) close();
        }
    });

    function attachAutocomplete(input) {
        const wrapper = input.parentElement;
        if (!wrapper) return;

        const dropdown = buildDropdown(wrapper);
        wireAriaCombobox(input, dropdown.id);

        // Mutable state for this input only.
        let suggestions = [];
        let activeIndex = -1;
        let composing = false;

        function closeDropdown() {
            dropdown.hidden = true;
            input.setAttribute("aria-expanded", "false");
            input.removeAttribute("aria-activedescendant");
            activeIndex = -1;
        }

        function refresh() {
            const songHits = searchDataset(input.value, songs, SONG_LIMIT);
            const artistHits = searchDataset(input.value, artists, ARTIST_LIMIT);

            suggestions = [];
            const html =
                renderSection("Piosenki", songHits, dropdown.id, suggestions) +
                renderSection("Artyści", artistHits, dropdown.id, suggestions);

            dropdown.innerHTML = html;
            activeIndex = -1;
            input.removeAttribute("aria-activedescendant");

            const hasResults = suggestions.length > 0;
            dropdown.hidden = !hasResults;
            input.setAttribute("aria-expanded", hasResults ? "true" : "false");
        }

        function refreshAfterLoad() {
            // Composition events fire mid-IME input; wait for end before searching.
            if (composing) return;
            if (songs === null || artists === null) {
                loadIndexes().then(refresh);
            } else {
                refresh();
            }
        }

        function setActiveItem(newIndex) {
            const items = dropdown.querySelectorAll(".pzt-suggest-item");
            if (items.length === 0) return;
            items.forEach((el) => el.classList.remove("is-active"));
            activeIndex = ((newIndex % items.length) + items.length) % items.length;
            const el = items[activeIndex];
            el.classList.add("is-active");
            el.scrollIntoView({ block: "nearest" });
            input.setAttribute("aria-activedescendant", el.id);
        }

        function goToActiveSuggestion() {
            if (activeIndex >= 0 && suggestions[activeIndex]) {
                window.location = suggestions[activeIndex].url;
            } else {
                submitSearchQuery();
            }
        }

        function submitSearchQuery() {
            const v = input.value.trim();
            if (v) window.location = SEARCH_PAGE + encodeURIComponent(v);
        }

        function findClickedItemIndex(target) {
            while (target && target !== dropdown && !target.classList.contains("pzt-suggest-item")) {
                target = target.parentNode;
            }
            if (!target || target === dropdown) return -1;
            const items = dropdown.querySelectorAll(".pzt-suggest-item");
            return Array.prototype.indexOf.call(items, target);
        }

        // --- Event wiring ---

        input.addEventListener("compositionstart", () => { composing = true; });
        input.addEventListener("compositionend", () => { composing = false; refreshAfterLoad(); });

        input.addEventListener("focus", () => {
            loadIndexes();
            // Help iOS keep the input visible above the soft keyboard.
            try { input.scrollIntoView({ block: "nearest" }); } catch (e) { /* noop */ }
        });

        input.addEventListener("input", refreshAfterLoad);

        input.addEventListener("keydown", (e) => {
            const dropdownClosed = dropdown.hidden || suggestions.length === 0;
            if (dropdownClosed) {
                if (e.key === "Enter") {
                    e.preventDefault();
                    submitSearchQuery();
                }
                return;
            }
            if (e.key === "ArrowDown") {
                e.preventDefault();
                setActiveItem(activeIndex + 1);
            } else if (e.key === "ArrowUp") {
                e.preventDefault();
                setActiveItem(activeIndex - 1);
            } else if (e.key === "Enter") {
                e.preventDefault();
                goToActiveSuggestion();
            } else if (e.key === "Escape") {
                closeDropdown();
            }
        });

        // pointerdown (not click) so navigation fires before the input's blur
        // event closes the dropdown.
        dropdown.addEventListener("pointerdown", (e) => {
            const idx = findClickedItemIndex(e.target);
            if (idx >= 0 && suggestions[idx]) {
                e.preventDefault();
                window.location = suggestions[idx].url;
            }
        });

        outsideClickHandlers.push({ wrapper, close: closeDropdown });
    }

    function buildDropdown(wrapper) {
        // The dropdown is absolute-positioned inside its wrapper, so the
        // wrapper must establish a positioning context.
        if (window.getComputedStyle(wrapper).position === "static") {
            wrapper.style.position = "relative";
        }
        const dropdown = document.createElement("ul");
        dropdown.id = "pzt-suggest-list-" + (++dropdownIdCounter);
        dropdown.className = "pzt-suggest-list";
        dropdown.setAttribute("role", "listbox");
        dropdown.hidden = true;
        wrapper.appendChild(dropdown);
        return dropdown;
    }

    function wireAriaCombobox(input, listId) {
        input.setAttribute("role", "combobox");
        input.setAttribute("aria-autocomplete", "list");
        input.setAttribute("aria-expanded", "false");
        input.setAttribute("aria-controls", listId);
        input.setAttribute("autocomplete", "off");
        input.setAttribute("spellcheck", "false");
    }


    // --- Boot ---------------------------------------------------------------

    document.addEventListener("DOMContentLoaded", () => {
        document.querySelectorAll(".search input").forEach(attachAutocomplete);
    });
}());
