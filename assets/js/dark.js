(function () {
    var ICONS = {
    sun: '<svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" aria-hidden="true"><circle cx="12" cy="12" r="4.5" stroke-width="1.2"/><line x1="12" y1="2" x2="12" y2="5" stroke-width="2" stroke-linecap="round"/><line x1="12" y1="19" x2="12" y2="22" stroke-width="2" stroke-linecap="round"/><line x1="2" y1="12" x2="5" y2="12" stroke-width="2" stroke-linecap="round"/><line x1="19" y1="12" x2="22" y2="12" stroke-width="2" stroke-linecap="round"/><line x1="4.93" y1="4.93" x2="7.05" y2="7.05" stroke-width="2" stroke-linecap="round"/><line x1="16.95" y1="16.95" x2="19.07" y2="19.07" stroke-width="2" stroke-linecap="round"/><line x1="4.93" y1="19.07" x2="7.05" y2="16.95" stroke-width="2" stroke-linecap="round"/><line x1="16.95" y1="7.05" x2="19.07" y2="4.93" stroke-width="2" stroke-linecap="round"/></svg>',
    moon: '<svg viewBox="0 0 24 24" fill="currentColor" stroke="none" aria-hidden="true"><path d="M10.1 2.2A10 10 0 1 0 20.9 16.5A9 9 0 0 1 10.1 2.2Z"/></svg>'
    };

    function applyTheme(isDark) {
        document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
        localStorage.setItem('pzt-theme', isDark ? 'dark' : 'light');
        document.querySelectorAll('.navbar-theme-toggle').forEach(function (btn) {
            btn.innerHTML = isDark ? ICONS.sun : ICONS.moon;
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        var isDark = document.documentElement.getAttribute('data-theme') === 'dark';

        document.querySelectorAll('.navbar-theme-toggle').forEach(function (btn) {
            btn.innerHTML = isDark ? ICONS.sun : ICONS.moon;
            btn.addEventListener('click', function () {
                isDark = !isDark;
                applyTheme(isDark);
            });
        });
    });
})();
