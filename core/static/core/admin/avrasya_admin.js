(function () {
    'use strict';

    function initDashboardDirectory() {
        var searchInput = document.getElementById('avDashSearch');
        var tabs = document.querySelectorAll('.av-cat-tab');
        var blocks = document.querySelectorAll('.av-category-block');
        if (!blocks.length) return;

        var activeCat = 'all';

        function applyFilters() {
            var q = searchInput ? searchInput.value.trim().toLowerCase() : '';
            blocks.forEach(function (block) {
                var catKey = block.getAttribute('data-cat');
                var catMatches = activeCat === 'all' || catKey === activeCat;

                if (!catMatches && !q) {
                    block.style.display = 'none';
                    return;
                }

                var cards = block.querySelectorAll('.av-app-card');
                var visibleCards = 0;

                cards.forEach(function (card) {
                    var appText = (card.getAttribute('data-search') || '').toLowerCase();
                    var rows = card.querySelectorAll('.av-model-row');
                    var appMatches = !q || appText.indexOf(q) !== -1;
                    var visibleRows = 0;

                    rows.forEach(function (row) {
                        var rowText = (row.getAttribute('data-search') || '').toLowerCase();
                        var showRow = appMatches || rowText.indexOf(q) !== -1;
                        row.style.display = showRow ? '' : 'none';
                        if (showRow) visibleRows += 1;
                    });

                    var showCard = visibleRows > 0;
                    card.style.display = showCard ? '' : 'none';
                    if (showCard) visibleCards += 1;
                });

                block.style.display = visibleCards > 0 ? '' : 'none';
                if (q && visibleCards > 0) {
                    block.classList.remove('is-collapsed');
                }
            });
        }

        tabs.forEach(function (tab) {
            tab.addEventListener('click', function () {
                tabs.forEach(function (t) { t.classList.remove('is-active'); });
                this.classList.add('is-active');
                activeCat = this.getAttribute('data-cat') || 'all';
                if (activeCat !== 'all') {
                    blocks.forEach(function (b) {
                        if (b.getAttribute('data-cat') === activeCat) {
                            b.classList.remove('is-collapsed');
                        }
                    });
                }
                applyFilters();
            });
        });

        document.querySelectorAll('.av-category-header').forEach(function (hdr) {
            hdr.addEventListener('click', function () {
                var block = this.closest('.av-category-block');
                if (block) {
                    block.classList.toggle('is-collapsed');
                }
            });
        });

        if (searchInput) {
            searchInput.addEventListener('input', applyFilters);
        }
    }

    function initCategorizedSidebar() {
        var filterInput = document.getElementById('nav-filter');
        var cats = document.querySelectorAll('.av-side-cat');
        if (!cats.length) return;

        document.querySelectorAll('.av-side-cat-btn').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var parent = this.closest('.av-side-cat');
                if (parent) parent.classList.toggle('is-open');
            });
        });

        // Auto-expand category containing current app
        cats.forEach(function (cat) {
            if (cat.querySelector('.current-app, .current-model')) {
                cat.classList.add('is-open');
            }
        });

        if (filterInput) {
            filterInput.addEventListener('input', function () {
                var q = this.value.trim().toLowerCase();
                cats.forEach(function (cat) {
                    var apps = cat.querySelectorAll('.av-side-app');
                    var visibleApps = 0;

                    apps.forEach(function (app) {
                        var appName = (app.getAttribute('data-search') || '').toLowerCase();
                        var items = app.querySelectorAll('.av-side-model-item');
                        var appMatch = !q || appName.indexOf(q) !== -1;
                        var visibleItems = 0;

                        items.forEach(function (item) {
                            var text = (item.getAttribute('data-search') || '').toLowerCase();
                            var show = appMatch || text.indexOf(q) !== -1;
                            item.style.display = show ? '' : 'none';
                            if (show) visibleItems += 1;
                        });

                        app.style.display = visibleItems > 0 ? '' : 'none';
                        if (visibleItems > 0) visibleApps += 1;
                    });

                    cat.style.display = visibleApps > 0 ? '' : 'none';
                    if (q && visibleApps > 0) {
                        cat.classList.add('is-open');
                    }
                });
            });
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        initDashboardDirectory();
        initCategorizedSidebar();
    });
})();
