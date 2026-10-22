from django import template
from django.utils.translation import gettext_lazy as _
from duyurular.models import Bolum
from kalite_akreditasyon.models import BolumKalite

register = template.Library()

TAB_DEFINITIONS = [
    ('tab1', _('FEDEK Akreditasyon Belgesi'), 'bi bi-award-fill'),
    ('tab2', _('Komisyon/Sorumlular'), 'bi bi-people-fill'),
    ('tab3', _('Program Öğretim Amaçları'), 'bi bi-bullseye'),
    ('tab4', _('Program Öğrenim Çıktıları'), 'bi bi-mortarboard-fill'),
    ('tab5', _('Anketler'), 'bi bi-bar-chart-line-fill'),
    ('tab6', _('Ders Planı'), 'bi bi-calendar3'),
]

@register.inclusion_tag('kalite_akreditasyon/includes/bolum_kalite_tabs.html', takes_context=True)
def render_bolum_kalite(context, bolum_kod=None):
    request = context.get('request')
    
    # Auto-detect if not explicitly provided
    if not bolum_kod and request:
        parts = [p for p in request.path.strip('/').split('/') if p]
        if parts:
            bolum_kod = parts[0]
            
    bolum = None
    if bolum_kod:
        bolum = Bolum.objects.filter(kod=bolum_kod).first()
        if not bolum:
            # Try alternate with hyphen or underscore
            alt_kod = bolum_kod.replace('_', '-') if '_' in bolum_kod else bolum_kod.replace('-', '_')
            bolum = Bolum.objects.filter(kod=alt_kod).first()
        if not bolum and bolum_kod in ['yeni_medya_iletisim', 'yeni-medya-iletisim']:
            bolum = Bolum.objects.filter(kod='yeni-medya-ve-iletisim').first()

    tabs_data = []
    if bolum:
        sekmeler = {s.sekme: s for s in BolumKalite.objects.filter(bolum=bolum, aktif=True).prefetch_related('dosyalar')}
        for key, default_title, icon in TAB_DEFINITIONS:
            sekme_obj = sekmeler.get(key)
            has_files = bool(sekme_obj and sekme_obj.dosyalar.exists())
            has_text = bool(sekme_obj and sekme_obj.icerik and sekme_obj.icerik.strip())
            tabs_data.append({
                'id': key,
                'default_title': default_title,
                'title': sekme_obj.baslik if (sekme_obj and sekme_obj.baslik) else default_title,
                'icon': icon,
                'obj': sekme_obj,
                'has_content': has_text or has_files,
                'dosyalar': sekme_obj.dosyalar.all() if sekme_obj else [],
            })
    else:
        for key, default_title, icon in TAB_DEFINITIONS:
            tabs_data.append({
                'id': key,
                'default_title': default_title,
                'title': default_title,
                'icon': icon,
                'obj': None,
                'has_content': False,
                'dosyalar': [],
            })

    return {
        'tabs_data': tabs_data,
        'bolum': bolum,
        'request': request,
    }
