function randomSong() {
    const links = document.querySelectorAll('#song-list a');
    if (links.length === 0) return;
    const idx = Math.floor(Math.random() * links.length);
    window.location.href = links[idx].href;
}

// Adds a dice next to the first mention of each artist on a song page. Randomly picks another song of that artist from /index/artists/<slug>.json.
(function () {
    const DICE = '<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><rect x="1.5" y="1.5" width="13" height="13" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="5" cy="5" r="1.3"/><circle cx="11" cy="5" r="1.3"/><circle cx="8" cy="8" r="1.3"/><circle cx="5" cy="11" r="1.3"/><circle cx="11" cy="11" r="1.3"/></svg>';

    function randomArtistSong(slug, btn) {
        let current = window.location.pathname;
        if (!current.endsWith('/')) current += '/';
        fetch('/index/artists/' + slug + '.json')
            .then((r) => (r.ok ? r.json() : []))
            .then((urls) => {
                const others = urls.filter((url) => url !== current);
                if (others.length === 0) {
                    btn.disabled = true;
                    return;
                }
                window.location.href = others[Math.floor(Math.random() * others.length)];
            });
    }

    document.addEventListener('DOMContentLoaded', function () {
        const seen = new Set();
        document.querySelectorAll('.song-info a[href^="/spiewnik/"]').forEach(function (link) {
            const slug = link.getAttribute('href').split('/')[2];
            if (!slug || seen.has(slug)) return;
            seen.add(slug);

            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'artist-random-dice d-print-none';
            btn.title = 'Losuj inną piosenkę: ' + link.textContent;
            btn.setAttribute('aria-label', btn.title);
            btn.innerHTML = DICE;
            btn.addEventListener('click', function () {
                randomArtistSong(slug, btn);
            });
            link.after(btn);
        });
    });
})();
