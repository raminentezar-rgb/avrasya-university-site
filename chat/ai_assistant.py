# chat/ai_assistant.py
"""Grounded AI support assistant backed by Avrasya University's whole-site search index and FAQs."""

import os
import re

from django.urls import reverse

from chat.models import SupportMessage
from support.models import FAQ
from support.services.search import normalize_ascii, normalize_tr, search_site_content


FILLER_WORDS = {
    'merhaba', 'selam', 'selamlar', 'gunaydin', 'iyi', 'gunler', 'aksamlar', 'lutfen',
    'acaba', 'bir', 'sey', 'sorum', 'var', 'olacaktim', 'olabilir', 'miyim', 'misiniz',
    'nedir', 'nelerdir', 'nerede', 'nasil', 'kimdir', 'kac', 'kactir', 'ne', 'zaman',
    'hakkinda', 'ilgili', 'bilgi', 'almak', 'istiyorum', 'verir', 'bilir', 'bakabilir',
    'bulabilirim', 'gorebilirim', 'ulabilirim', 'ulasabilirim', 'icin', 'veya', 'ile',
    'olan', 'icin', 'sayfasi', 'sayfasini', 'linki', 'link', 'adresi', 'mi', 'mu', 'mı',
    'mü', 'var', 'mi', 'yok', 'mu', 'ben', 'bana', 'benim', 'siz', 'size', 'sizin',
    'hello', 'hi', 'hey', 'please', 'where', 'what', 'how', 'can', 'find', 'info',
    'information', 'about', 'tell', 'give', 'the', 'for', 'and', 'with',
}

CROSS_LANG_TERM_MAP = {
    # English -> Turkish university terms
    'admission': 'aday ogrenci basvuru',
    'admissions': 'aday ogrenci basvuru',
    'applicant': 'aday ogrenci',
    'prospective': 'aday ogrenci',
    'tuition': 'ogrenim ucreti harc',
    'fee': 'ogrenim ucreti harc',
    'fees': 'ogrenim ucreti harc',
    'payment': 'online odeme taksit',
    'scholarship': 'burs indirim',
    'scholarships': 'burs indirim',
    'dormitory': 'konukevi barinma',
    'dorm': 'konukevi barinma',
    'guesthouse': 'konukevi barinma',
    'housing': 'konukevi barinma',
    'calendar': 'akademik takvim',
    'library': 'kutuphane',
    'cafeteria': 'yemekhane',
    'dining': 'yemekhane',
    'wifi': 'eduroam wifi internet',
    'engineering': 'muhendislik',
    'medicine': 'saglik bilimleri',
    'psychology': 'psikoloji',
    'nursing': 'hemsirelik',
    'graduate': 'lisansustu enstitu',
    'master': 'yuksek lisans tez',
    'erasmus': 'erasmus',
    'international': 'uluslararasi yabanci ogrenci',
    'contact': 'iletisim adres telefon',
    'dean': 'dekan yonetim',
    'registration': 'kayit islemleri',
    'register': 'kayit islemleri',
    'quality': 'kalite akreditasyon',
    # Persian -> Turkish university terms
    'پذیرش': 'aday ogrenci basvuru',
    'ثبت': 'kayit islemleri',
    'ثبتنام': 'kayit islemleri',
    'نام': 'kayit',
    'شهریه': 'ogrenim ucreti harc taksit',
    'هزینه': 'ogrenim ucreti harc',
    'بورس': 'burs indirim',
    'بورسیه': 'burs indirim',
    'خوابگاه': 'konukevi barinma',
    'سلف': 'yemekhane',
    'غذا': 'yemekhane',
    'کتابخانه': 'kutuphane',
    'تقویم': 'akademik takvim',
    'مهندسی': 'muhendislik',
    'روانشناسی': 'psikoloji',
    'پرستاری': 'hemsirelik',
    'ارشد': 'lisansustu yuksek lisans tez',
    'دکتری': 'doktora lisansustu enstitu',
    'اینترنت': 'eduroam wifi',
    'وای': 'eduroam wifi',
    'تماس': 'iletisim adres telefon',
    'آدرس': 'iletisim adres ulasim',
    'کیفیت': 'kalite akreditasyon',
}

GREETING_WORDS = {
    'merhaba', 'selam', 'selamlar', 'gunaydin', 'iyi gunler', 'iyi aksamlar',
    'hi', 'hello', 'hey', 'good morning', 'good afternoon',
    'سلام', 'درود', 'slm', 'mrb',
}

THANKS_WORDS = {
    'tesekkur', 'tesekkurler', 'sagol', 'sag ol', 'sagolun', 'eyvallah',
    'thanks', 'thank you', 'thx', 'ممنون', 'مرسی', 'تشکر', 'سپاس',
}

HANDOFF_PHRASES = (
    'canli destek', 'yetkili', 'temsilci', 'musteri hizmetleri', 'gercek kisi',
    'insan', 'gorevli', 'personel ile', 'biriyle gorusmek', 'operator',
    'live agent', 'human', 'talk to staff', 'support agent', 'real person',
    'اپراتور', 'پشتیبان', 'کارشناس', 'انسان', 'مسئول',
)


def _detect_lang(text, fallback='tr'):
    if re.search(r'[\u0600-\u06FF]', text or ''):
        return 'fa'
    norm_asc = normalize_ascii(text)
    en_markers = {'hello', 'hi', 'where', 'how', 'tuition', 'fee', 'fees', 'admission', 'scholarship', 'dormitory', 'human', 'please', 'thanks', 'thank', 'can', 'find', 'about'}
    words = set(norm_asc.split())
    if words & en_markers and not re.search(r'[çğıöşüÇĞİÖŞÜ]', text or ''):
        return 'en'
    return fallback if fallback in {'tr', 'en', 'fa'} else 'tr'


def _localized_text(lang, tr, en, fa):
    if lang == 'fa':
        return fa
    if lang == 'en':
        return en
    return tr


def _extract_semantic_query(raw_text):
    """Strip conversational fillers and translate key EN/FA terms to Turkish university search terms."""
    # Check for English/Persian keyword translations first
    raw_lower = (raw_text or '').lower()
    mapped_terms = []
    raw_words = re.findall(r'[\w\u0600-\u06FF]+', raw_lower)
    for w in raw_words:
        if w in CROSS_LANG_TERM_MAP:
            mapped_terms.append(CROSS_LANG_TERM_MAP[w])
        elif normalize_ascii(w) in CROSS_LANG_TERM_MAP:
            mapped_terms.append(CROSS_LANG_TERM_MAP[normalize_ascii(w)])

    norm_asc = normalize_ascii(raw_text)
    norm_tr = normalize_tr(raw_text)

    tokens_tr = norm_tr.split()
    kept_tr = []
    for tok in tokens_tr:
        if normalize_ascii(tok) not in FILLER_WORDS and len(tok) >= 2:
            kept_tr.append(tok)

    if mapped_terms:
        combined = ' '.join(kept_tr + mapped_terms).strip()
        return combined

    if kept_tr:
        return ' '.join(kept_tr)
    return norm_asc or raw_text.strip()


def _dedupe_links(links, max_links=3):
    seen = set()
    clean = []
    for lnk in links:
        url = (lnk.get('url') or '').strip()
        title = (lnk.get('title') or '').strip()
        if not url or not title or url in seen:
            continue
        seen.add(url)
        clean.append({'title': title[:65], 'url': url, 'category': lnk.get('category', '')})
        if len(clean) >= max_links:
            break
    return clean


def _try_openai_reply(question, lang, results, visitor_name):
    api_key = os.environ.get('OPENAI_API_KEY', '').strip()
    if not api_key:
        return None
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key, timeout=6.0)
        context_lines = []
        for idx, item in enumerate(results[:5], start=1):
            context_lines.append(
                f"{idx}. [{item.get('category', 'Bilgi')}] {item['title']} | URL: {item['url']}\n"
                f"   Özet: {item.get('content', '')[:300]}"
            )
        context_block = '\n'.join(context_lines) or 'Doğrudan eşleşen kayıt bulunamadı.'
        lang_instr = {
            'fa': 'Reply naturally in Persian (Farsi).',
            'en': 'Reply naturally in English.',
            'tr': 'Doğal, kibar ve net bir Türkçe ile yanıt ver.',
        }.get(lang, 'Türkçe yanıt ver.')

        resp = client.chat.completions.create(
            model=os.environ.get('OPENAI_MODEL', 'gpt-4o-mini'),
            temperature=0.2,
            max_tokens=280,
            messages=[
                {
                    'role': 'system',
                    'content': (
                        "Sen Avrasya Üniversitesi Akıllı Destek Asistanısın. "
                        f"{lang_instr} "
                        "Yalnızca aşağıda verilen Avrasya Üniversitesi kaynaklarına dayanarak kısa ve net yanıt ver. "
                        "Bağlam dışı sayı, isim veya URL uydurma. Linkler ayrıca buton olarak ekleneceği için metin içinde ham URL listelemek zorunda değilsin; kullanıcıyı ilgili sayfaya yönlendir."
                    ),
                },
                {
                    'role': 'user',
                    'content': f"Ziyaretçi ({visitor_name}) sorusu: {question}\n\nSite Kaynakları:\n{context_block}",
                },
            ],
        )
        content = (resp.choices[0].message.content or '').strip()
        return content or None
    except Exception:
        return None


def generate_ai_response(question, visitor_name='Ziyaretçi', session_lang='tr'):
    """Analyze visitor intent/query and return AI text, handoff flag, and verified page links."""
    q_clean = (question or '').strip()
    lang = _detect_lang(q_clean, fallback=session_lang)
    norm_asc = normalize_ascii(q_clean)

    # 1. Explicit request for human agent
    if any(phrase in norm_asc or phrase in q_clean.lower() for phrase in HANDOFF_PHRASES):
        return {
            'intent': 'handoff',
            'handoff': True,
            'text': _localized_text(
                lang,
                "Görüşmenizi canlı destek ekibimize yönlendirdim. Görevli personelimiz en kısa sürede bu pencereden size dönüş yapacaktır. Dilerseniz takip kodlu yazılı talep de oluşturabilirsiniz.",
                "I have transferred your conversation to our live support team. A staff member will reply here shortly. You can also open a tracked support ticket if needed.",
                "گفتگوی شما به کارشناسان پشتیبانی آنلاین ارجاع داده شد؛ همکاران ما در اولین فرصت از همین پنجره پاسخ می‌دهند. در صورت نیاز می‌توانید تیکت با کد پیگیری نیز ثبت کنید.",
            ),
            'links': [
                {'title': _localized_text(lang, 'Yeni Destek Talebi Aç', 'Create Support Ticket', 'ثبت تیکت پشتیبانی'), 'url': reverse('support:create_ticket'), 'category': 'Destek'},
            ],
        }

    # 2. Pure greeting (without a topic question)
    cleaned_words = set(norm_asc.split()) | set(q_clean.lower().split())
    if len(q_clean) <= 30 and (norm_asc in GREETING_WORDS or q_clean.lower() in GREETING_WORDS or (cleaned_words <= GREETING_WORDS and cleaned_words)):
        return {
            'intent': 'greeting',
            'handoff': False,
            'text': _localized_text(
                lang,
                f"Merhaba {visitor_name}! Ben Avrasya Üniversitesi Akıllı Asistanıyım. Fakülteler, bölümler, aday öğrenci, burslar, öğrenim ücretleri, kütüphane veya kampüs hakkında her şeyi sorabilirsiniz.",
                f"Hello {visitor_name}! I am the Avrasya University Smart Assistant. Ask me anything about admissions, programs, fees, scholarships, or campus services.",
                f"سلام {visitor_name}! من دستیار هوشمند دانشگاه اوراسیا هستم. می‌توانید درباره پذیرش، دانشکده‌ها، شهریه، بورسیه، خوابگاه و خدمات دانشگاه سوال بپرسید.",
            ),
            'links': [
                {'title': 'Aday Öğrenci Portalı', 'url': '/aday_ogrenci/', 'category': 'Portal'},
                {'title': 'Öğrenim Ücretleri', 'url': '/ogrenci_isleri/ogrenim_ucretleri/', 'category': 'Mali'},
                {'title': 'Sıkça Sorulan Sorular', 'url': reverse('support:faq_list'), 'category': 'SSS'},
            ],
        }

    # 3. Thanks / Closing
    if len(q_clean) <= 35 and (norm_asc in THANKS_WORDS or (cleaned_words & THANKS_WORDS and len(cleaned_words) <= 4)):
        return {
            'intent': 'thanks',
            'handoff': False,
            'text': _localized_text(
                lang,
                "Rica ederim! Başka bir sorunuz olursa buradan sorabilir veya canlı destek ekibimize bağlanabilirsiniz.",
                "You're welcome! Feel free to ask if you have any other questions.",
                "خواهش می‌کنم! اگر سوال دیگری دارید همین‌جا بپرسید یا به کارشناس پشتیبانی متصل شوید.",
            ),
            'links': [],
        }

    # 4. Whole-site smart search retrieval
    semantic_query = _extract_semantic_query(q_clean)
    results = search_site_content(semantic_query, lang_code='tr', limit=8)
    if not results and semantic_query != q_clean:
        results = search_site_content(q_clean, lang_code='tr', limit=8)

    if not results:
        return {
            'intent': 'fallback',
            'handoff': False,
            'text': _localized_text(
                lang,
                "Sorunuzla tam eşleşen bir sayfa bulamadım. İsterseniz site içi aramayı kullanabilir, yazılı destek talebi açabilir veya yukarıdaki 'Yetkiliye Bağlan' butonundan canlı ekibimize ulaşabilirsiniz.",
                "I couldn't find an exact page matching your question. You can browse full site search, submit a support ticket, or click 'Connect to Agent' above to chat with our staff.",
                "پاسخ دقیقی برای این سوال در صفحات سایت پیدا نکردم. می‌توانید از جستجوی کامل سایت استفاده کنید، تیکت ثبت کنید یا با دکمه «Yetkiliye Bağlan» به کارشناس پشتیبانی متصل شوید.",
            ),
            'links': [
                {'title': _localized_text(lang, 'Site İçi Aramaya Git', 'Search Site', 'جستجو در سایت'), 'url': f"{reverse('support:search')}?q={q_clean[:80]}", 'category': 'Arama'},
                {'title': _localized_text(lang, 'Destek Talebi Oluştur', 'Open Ticket', 'ثبت تیکت'), 'url': reverse('support:create_ticket'), 'category': 'Destek'},
            ],
        }

    # Build grounded clickable links from top results + relevant quick_links
    candidate_links = []
    top_hit = results[0]
    candidate_links.append({'title': top_hit['title'], 'url': top_hit['url'], 'category': top_hit.get('category', '')})
    for ql in top_hit.get('quick_links') or []:
        if len(candidate_links) >= 4:
            break
        candidate_links.append({'title': ql['title'], 'url': ql['url'], 'category': top_hit.get('category', '')})
    for extra in results[1:4]:
        if len(candidate_links) >= 4:
            break
        candidate_links.append({'title': extra['title'], 'url': extra['url'], 'category': extra.get('category', '')})
    curated_links = _dedupe_links(candidate_links, max_links=3)

    # Try optional LLM polish if key configured; otherwise use grounded deterministic composer
    llm_text = _try_openai_reply(q_clean, lang, results, visitor_name)
    if llm_text:
        return {
            'intent': 'answer',
            'handoff': False,
            'text': llm_text,
            'links': curated_links,
        }

    # Deterministic grounded synthesis
    if top_hit.get('type') == 'faq' and '/support/faq/' in (top_hit.get('url') or ''):
        faq_id_match = re.search(r'/support/faq/(\d+)/', top_hit['url'])
        full_answer = top_hit.get('content', '')
        if faq_id_match:
            faq_obj = FAQ.objects.filter(pk=int(faq_id_match.group(1)), is_active=True).first()
            if faq_obj:
                full_answer = faq_obj.answer
        if lang == 'fa':
            answer_text = f"پاسخ مرتبط ({top_hit['title']}):\n{full_answer}\n\nمی‌توانید از لینک‌های زیر مستقیم وارد صفحه مربوطه شوید:"
        elif lang == 'en':
            answer_text = f"{top_hit['title']}\n{full_answer}\n\nYou can open the relevant page(s) below:"
        else:
            answer_text = f"{full_answer}\n\nİlgili sayfaya aşağıdan doğrudan ulaşabilirsiniz:"
    else:
        snippet = (top_hit.get('content') or '').strip()
        if len(snippet) > 220:
            snippet = snippet[:217].rsplit(' ', 1)[0] + '...'
        if lang == 'fa':
            answer_text = f"مرتبط‌ترین نتیجه برای سوال شما «{top_hit['title']}» است.\n{snippet}\n\nلینک‌های مستقیم:"
        elif lang == 'en':
            answer_text = f"The best match for your question is \"{top_hit['title']}\".\n{snippet}\n\nDirect links:"
        else:
            intro = f"Aradığınız konu hakkında en ilgili sayfa: {top_hit['title']}"
            answer_text = f"{intro}\n{snippet}" if snippet else intro

    return {
        'intent': 'answer',
        'handoff': False,
        'text': answer_text,
        'links': curated_links,
    }


def maybe_reply_as_ai(thread, visitor_text, visitor_name='Ziyaretçi'):
    """Create and persist an AI reply on SupportThread unless human handoff is active."""
    if not thread or thread.human_handoff:
        return None

    res = generate_ai_response(visitor_text, visitor_name=visitor_name or thread.full_name or 'Ziyaretçi', session_lang=thread.language or 'tr')
    if res.get('handoff'):
        thread.human_handoff = True
        thread.save(update_fields=['human_handoff', 'updated_at'])

    ai_msg = SupportMessage.objects.create(
        thread=thread,
        sender_user=None,
        sender_name='Avrasya AI Asistan',
        text=res['text'],
        is_staff=True,
        is_ai=True,
        links=res.get('links') or [],
    )
    thread.is_active = True
    thread.save(update_fields=['is_active', 'updated_at'])
    return ai_msg
