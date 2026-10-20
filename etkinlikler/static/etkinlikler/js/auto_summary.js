/**
 * Avrasya Üniversitesi - Etkinlikler Modülü
 * Detaylı Açıklamadan Otomatik Özet (Kısa Açıklama) Oluşturma Scripti
 */

(function () {
    'use strict';

    // Otomatik Özet Üretici (JavaScript Uyarlaması)
    function generateSummaryJS(text, title, maxChars) {
        if (!text) return '';
        maxChars = maxChars || 320;

        // HTML etiketlerini ve boşlukları temizle
        let clean = text.replace(/<[^>]*>/g, ' ').replace(/&nbsp;/g, ' ');

        // Filtrelenecek meta satır başlangıçları ve emojiler
        const metaPrefixes = [
            'tarih:', 'saat:', 'yer:', 'eğitmen:', 'konuşmacı:', 'egitmen:', 'konusmaci:',
            'tarih :', 'saat :', 'yer :', 'date:', 'time:', 'location:', 'venue:', 'speaker:',
            'تاریخ:', 'ساعت:', 'مکان:', 'مدرس:', 'برگزارکننده:', 'datum:', 'zeit:', 'ort:',
            'дата:', 'время:', 'место:'
        ];
        const metaEmojis = ['📅', '🕒', '📍', '🗓️', '⏰', '📌', '👨‍🏫', '👩‍🏫', '🎯', '✨', '💚', '🔔', '📢'];

        const lines = clean.split('\n').map(l => l.trim()).filter(l => l.length > 0);
        const cleanedLines = [];

        const titleNorm = title ? title.replace(/[^a-zA-Z0-9\sğüşıöçĞÜŞİÖÇ]/g, '').toLowerCase().trim() : '';

        for (let l of lines) {
            const lLower = l.toLowerCase();
            if (metaPrefixes.some(p => lLower.startsWith(p))) continue;
            if (metaEmojis.some(e => l.startsWith(e))) continue;

            const lNorm = l.replace(/[^a-zA-Z0-9\sğüşıöçĞÜŞİÖÇ]/g, '').toLowerCase().trim();
            // Başlıkla birebir aynı veya çok kısa başlıksı satırları atla
            if (titleNorm && (lNorm === titleNorm || (lNorm.length < 60 && titleNorm.includes(lNorm)))) {
                continue;
            }
            // Kısa ve noktalama işareti veya yüklem olmayan satırları atla
            if (l.length < 55 && !/[.!?:]$/.test(l) && !/(dir|tir|dır|tır|cek|cak|miş|mış|yor|du|dü|dı|di)$/i.test(l)) {
                continue;
            }

            if (!/[.!?]$/.test(l)) {
                l += '.';
            }
            cleanedLines.push(l);
        }

        const combined = cleanedLines.join(' ').replace(/\s+/g, ' ').trim();
        if (!combined) {
            return clean.substring(0, maxChars).trim();
        }

        // Cümlelere böl
        const sentenceRegex = /[^.!?]+[.!?]+/g;
        const sentences = combined.match(sentenceRegex) || [combined];

        const selected = [];
        let currLen = 0;

        for (let s of sentences) {
            const sClean = s.trim();
            if (!sClean || sClean.length < 15) continue;
            selected.push(sClean);
            currLen += sClean.length;
            if (currLen >= 200 || selected.length >= 2) {
                if (currLen >= 180) break;
            }
        }

        if (selected.length === 0) {
            return combined.substring(0, maxChars).trim();
        }

        let summary = selected.join(' ');
        if (summary.length > maxChars + 80) {
            summary = summary.substring(0, maxChars);
            const lastSpace = summary.lastIndexOf(' ');
            if (lastSpace > 0) summary = summary.substring(0, lastSpace);
            if (!/[.!?]$/.test(summary)) summary += '...';
        }
        return summary;
    }

    function initAutoSummary() {
        // Detaylı Açıklama alanlarını tara (tr, en, fa, ar, ru, de ve varsayılan)
        const detayTextareas = document.querySelectorAll('textarea[name^="detayli_aciklama"]');
        if (!detayTextareas || detayTextareas.length === 0) return;

        detayTextareas.forEach(detayEl => {
            const name = detayEl.getAttribute('name');
            // İlgili kısa açıklama alanının adını bul (ör: detayli_aciklama_tr -> kisa_aciklama_tr)
            const kisaName = name.replace('detayli_aciklama', 'kisa_aciklama');
            const kisaEl = document.querySelector(`textarea[name="${kisaName}"]`);
            if (!kisaEl) return;

            // İlgili başlık alanını bul
            const baslikName = name.replace('detayli_aciklama', 'baslik');
            const baslikEl = document.querySelector(`input[name="${baslikName}"]`);

            // Eğer zaten toolbar eklenmişse tekrar ekleme
            const existingBar = kisaEl.parentElement.querySelector('.auto-summary-toolbar');
            if (existingBar) return;

            // Toolbar oluştur
            const toolbar = document.createElement('div');
            toolbar.className = 'auto-summary-toolbar';
            toolbar.innerHTML = `
                <div class="auto-summary-btn-wrap">
                    <button type="button" class="btn-auto-summary" title="Detaylı açıklamadan otomatik özet üretir">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> ✨ Otomatik Özet Oluştur
                    </button>
                    <span class="auto-summary-badge">
                        <i class="fa-solid fa-bolt"></i> Detaylı metin yapıştırıldığında özet otomatik üretilir
                    </span>
                    <span class="auto-summary-count" style="display: none;"></span>
                </div>
            `;

            kisaEl.parentElement.insertBefore(toolbar, kisaEl);

            const btn = toolbar.querySelector('.btn-auto-summary');
            const badge = toolbar.querySelector('.auto-summary-badge');
            const countBadge = toolbar.querySelector('.auto-summary-count');

            function triggerSummary(force) {
                const detayText = (detayEl.value || '').trim();
                const kisaText = (kisaEl.value || '').trim();
                const titleText = baslikEl ? (baslikEl.value || '').trim() : '';

                if (!detayText) return;

                // Eğer zorlama değilse ve kısa açıklama elle doldurulmuşsa (ve detayla birebir aynı değilse), dokunma
                if (!force && kisaText && kisaText !== detayText && !kisaEl.dataset.isAuto) {
                    return;
                }

                const summary = generateSummaryJS(detayText, titleText, 320);
                if (summary) {
                    kisaEl.value = summary;
                    kisaEl.dataset.isAuto = 'true';
                    
                    // Görsel bildirim
                    kisaEl.classList.remove('pulse-highlight');
                    void kisaEl.offsetWidth; // DOM reflow
                    kisaEl.classList.add('pulse-highlight');

                    badge.innerHTML = `<span style="color: #10b981; font-weight: 600;"><i class="fa-solid fa-check"></i> Özet otomatik oluşturuldu (${summary.length} karakter)</span>`;
                    if (countBadge) {
                        countBadge.style.display = 'inline-block';
                        countBadge.textContent = `${summary.length} karakter`;
                    }
                }
            }

            // Butona basıldığında
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                triggerSummary(true);
            });

            // Detaylı metin girildiğinde veya yapıştırıldığında
            detayEl.addEventListener('input', function () {
                triggerSummary(false);
            });

            detayEl.addEventListener('paste', function () {
                setTimeout(function () {
                    triggerSummary(false);
                }, 100);
            });

            // Kullanıcı kısa açıklamayı kendisi düzenlerse otomatik bayrağını kaldır
            kisaEl.addEventListener('input', function () {
                delete kisaEl.dataset.isAuto;
                badge.innerHTML = `<span style="color: #64748b;"><i class="fa-solid fa-pencil"></i> Manuel düzenlendi (${kisaEl.value.length} karakter)</span>`;
            });
        });
    }

    // Sayfa yüklendiğinde ve dinamik tab geçişlerinde çalıştır
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAutoSummary);
    } else {
        initAutoSummary();
    }

    // Modeltranslation tab değişimlerini dinle
    document.addEventListener('click', function (e) {
        if (e.target && e.target.closest('.ui-tabs-anchor, .changeform-tabs-item')) {
            setTimeout(initAutoSummary, 150);
        }
    });

    // FontAwesome desteği
    if (!document.getElementById('font-awesome-cdn')) {
        const fa = document.createElement('link');
        fa.id = 'font-awesome-cdn';
        fa.rel = 'stylesheet';
        fa.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css';
        document.head.appendChild(fa);
    }
})();
