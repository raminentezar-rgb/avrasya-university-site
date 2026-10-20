/**
 * Avrasya Üniversitesi - Haberler Modülü
 * Haber İçeriğinden Akıllı ve Profesyonel Otomatik Özet Oluşturma Scripti
 * (Etkinlikler modülü ile birebir aynı standartta çalışır)
 */

(function () {
    'use strict';

    // Akıllı Çok Boyutlu Haber Özeti Üretici (Giriş, Gelişme ve Sonuç Sentezi)
    function generateNewsSummaryJS(text, title, maxChars) {
        if (!text) return '';
        maxChars = maxChars || 360;

        // HTML etiketlerini ve boşlukları temizle
        let clean = text.replace(/<[^>]*>/g, ' ').replace(/&nbsp;/g, ' ');

        // Filtrelenecek meta satır başlangıçları ve emojiler
        const metaPrefixes = [
            'tarih:', 'saat:', 'yer:', 'kaynak:', 'muhabir:', 'yazar:', 'eğitmen:', 'konuşmacı:',
            'egitmen:', 'konusmaci:', 'tarih :', 'saat :', 'yer :', 'date:', 'time:', 'source:', 
            'author:', 'location:', 'venue:', 'speaker:', 'تاریخ:', 'ساعت:', 'مکان:', 'منبع:', 
            'نویسنده:', 'خبرنگار:', 'datum:', 'zeit:', 'ort:', 'quelle:', 'дата:', 'время:', 'место:'
        ];
        const metaEmojis = ['📅', '🕒', '📍', '🗓️', '⏰', '📌', '📰', '📢', '🎯', '✨', '💚', '🔔', '🎤', '📸'];

        const lines = clean.split('\n').map(l => l.trim()).filter(l => l.length > 0);
        const filteredParas = [];

        const titleNorm = title ? title.replace(/[^a-zA-Z0-9\sğüşıöçĞÜŞİÖÇ]/g, '').toLowerCase().trim() : '';

        for (let l of lines) {
            const lLower = l.toLowerCase();
            if (metaPrefixes.some(p => lLower.startsWith(p))) continue;
            if (metaEmojis.some(e => l.startsWith(e))) continue;

            const lNorm = l.replace(/[^a-zA-Z0-9\sğüşıöçĞÜŞİÖÇ]/g, '').toLowerCase().trim();
            if (titleNorm && (lNorm === titleNorm || (lNorm.length < 60 && titleNorm.includes(lNorm)))) {
                continue;
            }
            if (l.length < 30 && !/[.!?:]$/.test(l) && !/(dir|tir|dır|tır|cek|cak|miş|mış|yor|du|dü|dı|di)$/i.test(l)) {
                continue;
            }
            filteredParas.push(l);
        }

        if (filteredParas.length === 0) {
            return clean.substring(0, maxChars).trim();
        }

        // Paragrafları cümlelerine böl
        const parsedParas = [];
        for (let p of filteredParas) {
            const sentenceRegex = /[^.!?。؛]+[.!?。؛]+/g;
            const matches = p.match(sentenceRegex) || [p];
            const cleanSents = matches.map(s => s.trim()).filter(s => s.length > 15);
            if (cleanSents.length > 0) {
                parsedParas.push(cleanSents);
            }
        }

        if (parsedParas.length === 0) {
            return filteredParas[0].substring(0, maxChars).trim();
        }

        // 1. Giriş cümlesini al ve gerekirse bürokratik kalıplardan arındır
        const leadSents = parsedParas[0];
        let condensedLead = leadSents[0];

        const quoteMatch = condensedLead.match(/[“"']([^”"']+)[”"']/);
        const quoteTitle = quoteMatch ? quoteMatch[1] : '';

        if (condensedLead.length > 130 && quoteTitle) {
            const verbs = ['düzenlendi', 'gerçekleştirildi', 'yapıldı', 'buluştu', 'başladı', 'gerçekleştirilmiştir'];
            if (condensedLead.includes('tarafından') && verbs.some(v => condensedLead.includes(v))) {
                const orgMatch = condensedLead.match(/(?:Üniversitemiz\s+)?([A-ZÇĞİÖŞÜa-zçğıöşü\s,]+?)\s+tarafından/);
                const org = orgMatch ? orgMatch[1].trim() : '';
                if (org && org.length < 80) {
                    condensedLead = `${org} tarafından düzenlenen “${quoteTitle}” etkinliğinde öğrenciler bir araya geldi.`;
                } else {
                    condensedLead = `Avrasya Üniversitesi'nde “${quoteTitle}” etkinliği gerçekleştirildi.`;
                }
            }
        }

        // 2. Gelişme / Detay cümlesi (eylem, atölye, katılım)
        const actionVerbs = [
            'fırsatı buldu', 'katıldı', 'deneyimledi', 'keşfetti', 'paylaştı', 'bilgi aldı',
            'dinledi', 'sağlayarak', 'sağladı', 'ele alındı', 'gerçekleştirdi', 'aktardı',
            'konuştu', 'değerlendirdi', 'sundu', 'vurguladı', 'bir araya gelerek'
        ];

        let activitySent = '';
        if (parsedParas.length > 1) {
            const middleParas = parsedParas.length > 2 ? parsedParas.slice(1, -1) : [parsedParas[1]];
            const bodySents = [];
            for (let mp of middleParas) {
                bodySents.push(...mp);
            }
            for (let s of bodySents) {
                const sLower = s.toLowerCase();
                if (actionVerbs.some(v => sLower.includes(v))) {
                    activitySent = s;
                    break;
                }
            }
            if (!activitySent && bodySents.length > 0) {
                activitySent = bodySents[0];
            }
        } else if (leadSents.length > 1) {
            for (let s of leadSents.slice(1)) {
                const sLower = s.toLowerCase();
                if (actionVerbs.some(v => sLower.includes(v))) {
                    activitySent = s;
                    break;
                }
            }
            if (!activitySent) {
                activitySent = leadSents[1];
            }
        }

        // 3. Sonuç / Etki cümlesi (varsa)
        let outcomeSent = '';
        if (parsedParas.length >= 3) {
            const lastSents = parsedParas[parsedParas.length - 1];
            const impactVerbs = ['katkı sağladı', 'güçlenmesine', 'hedefledi', 'amaçlandı', 'tamamlandı', 'sona erdi', 'vurgulandı', 'memnuniyetini belirtti'];
            for (let s of lastSents) {
                const sLower = s.toLowerCase();
                if (impactVerbs.some(v => sLower.includes(v)) && s !== activitySent) {
                    outcomeSent = s;
                    break;
                }
            }
        }

        const chosen = [condensedLead];
        let currentLen = condensedLead.length;

        if (activitySent && activitySent !== condensedLead) {
            chosen.push(activitySent);
            currentLen += activitySent.length;
        }

        if (outcomeSent && !chosen.includes(outcomeSent) && currentLen + outcomeSent.length <= maxChars + 60) {
            chosen.push(outcomeSent);
        }

        let summary = chosen.join(' ');
        if (summary.length > maxChars + 80) {
            summary = summary.substring(0, maxChars);
            const lastSpace = summary.lastIndexOf(' ');
            if (lastSpace > 0) summary = summary.substring(0, lastSpace);
            if (!/[.!?]$/.test(summary)) summary += '...';
        }
        return summary;
    }

    function initAutoSummary() {
        const summaryTextareas = document.querySelectorAll('textarea[name^="summary"]');
        if (!summaryTextareas || summaryTextareas.length === 0) return;

        summaryTextareas.forEach(summaryEl => {
            // Eğer zaten toolbar eklenmişse tekrar ekleme
            const existingBar = summaryEl.parentElement.querySelector('.auto-summary-toolbar');
            if (existingBar) return;

            // İlgili veya aktif içerik alanını bulucu
            function getBestContentElement() {
                // 1. summary adıyla eşleşen (örn: summary_tr -> content_tr)
                const sName = summaryEl.getAttribute('name');
                if (sName && sName !== 'summary') {
                    const matchedContent = document.querySelector(`textarea[name="${sName.replace('summary', 'content')}"]`);
                    if (matchedContent) return matchedContent;
                }

                // 2. Görünür/aktif sekmedeki içerik alanı
                const allContents = document.querySelectorAll('textarea[name^="content"]');
                for (let c of allContents) {
                    if (c.offsetParent !== null && (c.value || '').trim()) {
                        return c;
                    }
                }

                // 3. Sırasıyla content_tr, content, content_en veya metin barındıran ilk alan
                const contentTr = document.querySelector('textarea[name="content_tr"]');
                if (contentTr && (contentTr.value || '').trim()) return contentTr;

                const contentDef = document.querySelector('textarea[name="content"]');
                if (contentDef && (contentDef.value || '').trim()) return contentDef;

                for (let c of allContents) {
                    if ((c.value || '').trim()) return c;
                }

                return contentTr || contentDef || allContents[0];
            }

            function getBestTitle() {
                const titleTr = document.querySelector('input[name="title_tr"]');
                if (titleTr && titleTr.value.trim()) return titleTr.value.trim();
                const titleDef = document.querySelector('input[name="title"]');
                if (titleDef && titleDef.value.trim()) return titleDef.value.trim();
                const anyTitle = document.querySelector('input[name^="title"]');
                return anyTitle ? anyTitle.value.trim() : '';
            }

            // Toolbar oluştur
            const toolbar = document.createElement('div');
            toolbar.className = 'auto-summary-toolbar';
            toolbar.innerHTML = `
                <div class="auto-summary-btn-wrap">
                    <button type="button" class="btn-auto-summary" title="Haber içeriğinden otomatik, anlamlı özet üretir">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> ✨ Otomatik Özet Oluştur
                    </button>
                    <span class="auto-summary-badge">
                        <i class="fa-solid fa-bolt"></i> İçerik girildiğinde özet otomatik üretilir
                    </span>
                    <span class="auto-summary-count" style="display: none;"></span>
                </div>
            `;

            summaryEl.parentElement.insertBefore(toolbar, summaryEl);

            const btn = toolbar.querySelector('.btn-auto-summary');
            const badge = toolbar.querySelector('.auto-summary-badge');
            const countBadge = toolbar.querySelector('.auto-summary-count');

            // Eğer mevcut özet varsa karakter sayısını göster
            if (summaryEl.value && summaryEl.value.trim()) {
                const len = summaryEl.value.trim().length;
                countBadge.style.display = 'inline-block';
                countBadge.textContent = `${len} karakter`;
            }

            function triggerSummary(force) {
                const contentEl = getBestContentElement();
                if (!contentEl) return;

                const contentText = (contentEl.value || '').trim();
                const summaryText = (summaryEl.value || '').trim();
                const titleText = getBestTitle();

                if (!contentText) return;

                // Eğer zorlama buton tıklaması değilse ve özet zaten elle doldurulmuşsa (ve içerikle aynı değilse ve hatalı kesik '...' ile bitmiyorsa), dokunma
                if (!force && summaryText && summaryText !== contentText && !summaryText.endsWith('...') && !summaryEl.dataset.isAuto) {
                    return;
                }

                const summary = generateNewsSummaryJS(contentText, titleText, 350);
                if (summary) {
                    summaryEl.value = summary;
                    summaryEl.dataset.isAuto = 'true';

                    // Görsel bildirim (parlama animasyonu)
                    summaryEl.classList.remove('pulse-highlight');
                    void summaryEl.offsetWidth; // DOM reflow
                    summaryEl.classList.add('pulse-highlight');

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

            // Tüm içerik alanlarını dinle (yazıldığında veya yapıştırıldığında)
            const allContentElements = document.querySelectorAll('textarea[name^="content"]');
            allContentElements.forEach(cntEl => {
                cntEl.addEventListener('input', function () {
                    triggerSummary(false);
                });

                cntEl.addEventListener('paste', function () {
                    setTimeout(function () {
                        triggerSummary(false);
                    }, 100);
                });
            });

            // Kullanıcı özeti kendisi elle düzenlerse bayrağı kaldır
            summaryEl.addEventListener('input', function () {
                delete summaryEl.dataset.isAuto;
                const len = summaryEl.value.length;
                badge.innerHTML = `<span style="color: #64748b;"><i class="fa-solid fa-pencil"></i> Manuel düzenlendi (${len} karakter)</span>`;
                if (countBadge) {
                    countBadge.style.display = 'inline-block';
                    countBadge.textContent = `${len} karakter`;
                }
            });
        });
    }

    // Sayfa yüklendiğinde çalıştır
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAutoSummary);
    } else {
        initAutoSummary();
    }

    // Modeltranslation veya sekme değişimlerinde tekrar tetikle
    document.addEventListener('click', function (e) {
        if (e.target && e.target.closest('.ui-tabs-anchor, .changeform-tabs-item, .grp-tab-button')) {
            setTimeout(initAutoSummary, 150);
        }
    });

    // FontAwesome desteğini ekle
    if (!document.getElementById('font-awesome-cdn')) {
        const fa = document.createElement('link');
        fa.id = 'font-awesome-cdn';
        fa.rel = 'stylesheet';
        fa.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css';
        document.head.appendChild(fa);
    }
})();
