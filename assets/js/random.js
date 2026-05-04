function randomSong() {
    const links = document.querySelectorAll('#song-list a');
    if (links.length === 0) return;
    const idx = Math.floor(Math.random() * links.length);
    window.location.href = links[idx].href;
}
