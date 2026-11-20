from django import template
from django.utils.translation import gettext_lazy as _
from akademik.models import FakulteSayfasi, BolumSayfasi

register = template.Library()

BOLUM_KOD_ALIASES = {
    'gorsel-iletisim-tasarimi': 'gorsel_iletisim_tasarimi',
    'yeni-medya-ve-iletisim': 'yeni_medya_iletisim',
    'yeni-medya-iletisim': 'yeni_medya_iletisim',
}


def _detect_code_from_request(request, fallback=None):
    if fallback:
        return BOLUM_KOD_ALIASES.get(fallback, fallback)
    if request:
        parts = [p for p in request.path.strip('/').split('/') if p]
        # Skip language prefix (tr, en, fa, ar, ru, de) if present
        if parts and parts[0] in ('tr', 'en', 'fa', 'ar', 'ru', 'de') and len(parts) > 1:
            kod = parts[1]
        elif parts:
            kod = parts[0]
        else:
            kod = ''
        return BOLUM_KOD_ALIASES.get(kod, kod)
    return ''


@register.simple_tag(takes_context=True)
def get_fakulte_sayfasi(context, fakulte_kodu=None):
    request = context.get('request')
    kod = _detect_code_from_request(request, fakulte_kodu)
    if not kod:
        return None
    return (
        FakulteSayfasi.objects.filter(fakulte_kodu=kod, aktif=True)
        .prefetch_related('bolum_kartlari', 'ek_yoneticiler', 'ek_sekmeler')
        .first()
    )


@register.simple_tag
def localized_val(obj, field_name, default=''):
    if obj is None:
        return default
    if hasattr(obj, 'get_localized'):
        val = obj.get_localized(field_name, default)
        return val if val else default
    return getattr(obj, field_name, None) or default


@register.inclusion_tag('akademik/includes/bolum_dinamik_tabs.html', takes_context=True)
def render_bolum_sayfasi(context, bolum_kodu=None):
    request = context.get('request')
    kod = _detect_code_from_request(request, bolum_kodu)

    bolum_obj = None
    if kod:
        bolum_obj = (
            BolumSayfasi.objects.filter(bolum_kodu=kod, aktif=True)
            .select_related('bolum')
            .prefetch_related('ek_yoneticiler', 'ek_sekmeler', 'akademik_kadro')
            .first()
        )
        if not bolum_obj:
            alt = kod.replace('-', '_') if '-' in kod else kod.replace('_', '-')
            bolum_obj = (
                BolumSayfasi.objects.filter(bolum_kodu=alt, aktif=True)
                .select_related('bolum')
                .prefetch_related('ek_yoneticiler', 'ek_sekmeler', 'akademik_kadro')
                .first()
            )

    if bolum_obj:
        bolum_adi = bolum_obj.get_localized('bolum_adi', kod.replace('_', ' ').title())
        kadro_qs = bolum_obj.akademik_kadro.filter(aktif=True)
        kadro_uyeleri = []
        misafir_uyeleri = []
        for uye in kadro_qs:
            item = {
                'ad_soyad': uye.ad_soyad,
                'unvan_gorev': uye.get_localized('unvan_gorev', _('Öğretim Üyesi')),
                'uzmanlik_alani': uye.get_localized('uzmanlik_alani'),
                'eposta': uye.eposta,
                'telefon': uye.telefon,
                'oda': uye.oda,
                'ozgecmis_url': uye.ozgecmis_url,
                'fotograf': uye.fotograf,
                'biyografi': uye.get_localized('biyografi'),
            }
            if uye.kadro_turu == 'misafir':
                misafir_uyeleri.append(item)
            else:
                kadro_uyeleri.append(item)
        ek_yoneticiler = [
            {
                'ad_soyad': y.ad_soyad,
                'gorev': y.get_localized('gorev'),
                'eposta': y.eposta,
                'telefon': y.telefon,
                'fotograf': y.fotograf,
                'ozgecmis_url': y.ozgecmis_url,
            }
            for y in bolum_obj.ek_yoneticiler.filter(aktif=True)
        ]
        ek_sekmeler = [
            {
                'id': f'ek_{sek.id}',
                'baslik': sek.get_localized('baslik'),
                'alt_baslik': sek.get_localized('alt_baslik'),
                'ikon': sek.ikon or 'fas fa-layer-group',
                'icerik': sek.get_localized('icerik'),
            }
            for sek in bolum_obj.ek_sekmeler.filter(aktif=True)
        ]
        data = {
            'exists': True,
            'bolum_adi': bolum_adi,
            'fakulte_adi': bolum_obj.get_localized('fakulte_adi'),
            'program_turu': bolum_obj.get_localized('program_turu', _('Lisans Programı')),
            'tarihce_sekme': bolum_obj.get_localized('tarihce_baslik', _('Tarihçe')),
            'tarihce_baslik': bolum_obj.get_localized('tarihce_alt_baslik') or f"{bolum_adi} {_('Tarihçesi')}",
            'tarihce_icerik': bolum_obj.get_localized('tarihce_icerik'),
            'mv_sekme': bolum_obj.get_localized('misyon_vizyon_baslik', _('Misyon & Vizyon')),
            'mv_baslik': bolum_obj.get_localized('misyon_vizyon_alt_baslik') or f"{bolum_adi} {_('Misyon ve Vizyonu')}",
            'misyon_icerik': bolum_obj.get_localized('misyon_icerik'),
            'vizyon_icerik': bolum_obj.get_localized('vizyon_icerik'),
            'amaclari_icerik': bolum_obj.get_localized('amaclari_icerik'),
            'ne_is_sekme': bolum_obj.get_localized('ne_is_yaparlar_baslik', _('Ne İş Yaparlar?')),
            'ne_is_baslik': bolum_obj.get_localized('ne_is_yaparlar_alt_baslik') or f"{bolum_adi} {_('Mezunları Ne İş Yaparlar?')}",
            'ne_is_icerik': bolum_obj.get_localized('ne_is_yaparlar_icerik'),
            'mezun_sekme': bolum_obj.get_localized('mezunlar_calisma_baslik', _('Mezunlar Nerede Çalışırlar?')),
            'mezun_baslik': bolum_obj.get_localized('mezunlar_calisma_alt_baslik') or _('Mezunlar Nerede Çalışırlar?'),
            'mezun_icerik': bolum_obj.get_localized('mezunlar_calisma_icerik'),
            'yonetim_sekme': bolum_obj.get_localized('yonetim_baslik', _('Yönetim')),
            'yonetim_baslik': bolum_obj.get_localized('yonetim_alt_baslik', _('Bölüm Yönetimi')),
            'baskan_unvan_ad': bolum_obj.baskan_unvan_ad,
            'baskan_gorev_etiketi': bolum_obj.get_localized('baskan_gorev_etiketi', _('Bölüm Başkanı')),
            'baskan_unvan_detay': bolum_obj.get_localized('baskan_unvan_detay'),
            'baskan_eposta': bolum_obj.baskan_eposta,
            'baskan_telefon': bolum_obj.baskan_telefon,
            'baskan_oda': bolum_obj.baskan_oda,
            'baskan_ofis_saatleri': bolum_obj.baskan_ofis_saatleri,
            'baskan_fotograf': bolum_obj.baskan_fotograf,
            'baskan_ozgecmis_url': bolum_obj.baskan_ozgecmis_url,
            'baskan_mesaji': bolum_obj.get_localized('baskan_mesaji'),
            'kadro_sekme': bolum_obj.get_localized('kadro_baslik', _('Akademik Kadro')),
            'kadro_baslik': bolum_obj.get_localized('kadro_alt_baslik', _('Akademik Kadro')),
            'kadro_aciklama': bolum_obj.get_localized('kadro_aciklama'),
            'kadro_uyeleri': kadro_uyeleri,
            'misafir_uyeleri': misafir_uyeleri,
            'kadro_toplam': len(kadro_uyeleri) + len(misafir_uyeleri),
            'ek_yoneticiler': ek_yoneticiler,
            'ek_sekmeler': ek_sekmeler,
        }
    else:
        data = {
            'exists': False,
            'bolum_adi': kod.replace('_', ' ').title(),
            'fakulte_adi': '',
            'program_turu': '',
            'tarihce_sekme': _('Tarihçe'),
            'tarihce_baslik': _('Tarihçe'),
            'tarihce_icerik': '',
            'mv_sekme': _('Misyon & Vizyon'),
            'mv_baslik': _('Misyon & Vizyon'),
            'misyon_icerik': '',
            'vizyon_icerik': '',
            'amaclari_icerik': '',
            'ne_is_sekme': _('Ne İş Yaparlar?'),
            'ne_is_baslik': _('Mezunlar Ne İş Yaparlar?'),
            'ne_is_icerik': '',
            'mezun_sekme': _('Mezunlar Nerede Çalışırlar?'),
            'mezun_baslik': _('Mezunlar Nerede Çalışırlar?'),
            'mezun_icerik': '',
            'yonetim_sekme': _('Yönetim'),
            'yonetim_baslik': _('Bölüm Yönetimi'),
            'baskan_unvan_ad': '',
            'baskan_gorev_etiketi': '',
            'baskan_unvan_detay': '',
            'baskan_eposta': '',
            'baskan_telefon': '',
            'baskan_oda': '',
            'baskan_ofis_saatleri': '',
            'baskan_fotograf': None,
            'baskan_ozgecmis_url': '',
            'baskan_mesaji': '',
            'kadro_sekme': _('Akademik Kadro'),
            'kadro_baslik': _('Akademik Kadro'),
            'kadro_aciklama': '',
            'kadro_uyeleri': [],
            'misafir_uyeleri': [],
            'kadro_toplam': 0,
            'ek_yoneticiler': [],
            'ek_sekmeler': [],
        }

    return {
        'd': data,
        'bolum_obj': bolum_obj,
        'request': request,
    }


@register.inclusion_tag('akademik/includes/fakulte_tab_header.html', takes_context=True)
def render_fakulte_tab_header(context, fakulte_sayfasi=None):
    ek_sekmeler = []
    if fakulte_sayfasi:
        for sek in fakulte_sayfasi.ek_sekmeler.filter(aktif=True):
            ek_sekmeler.append({
                'id': f'ek_{sek.id}',
                'baslik': sek.get_localized('baslik'),
                'ikon': sek.ikon or 'fas fa-layer-group',
            })
        show_bolumler = fakulte_sayfasi.bolumler_sekmesi_goster
        bolumler_baslik = fakulte_sayfasi.get_localized('bolumler_baslik', _('Bölümler'))
        tarihce_baslik = fakulte_sayfasi.get_localized('tarihce_baslik', _('Tarihçe'))
        mv_baslik = fakulte_sayfasi.get_localized('misyon_vizyon_baslik', _('Misyon & Vizyon'))
        mesaj_baslik = fakulte_sayfasi.get_localized('mesaj_sekme_adi', _('Dekan Mesajı'))
    else:
        show_bolumler = True
        bolumler_baslik = _('Bölümler')
        tarihce_baslik = _('Tarihçe')
        mv_baslik = _('Misyon & Vizyon')
        mesaj_baslik = _('Dekan Mesajı')

    return {
        'show_bolumler': show_bolumler,
        'bolumler_baslik': bolumler_baslik,
        'tarihce_baslik': tarihce_baslik,
        'mv_baslik': mv_baslik,
        'mesaj_baslik': mesaj_baslik,
        'ek_sekmeler': ek_sekmeler,
    }


@register.inclusion_tag('akademik/includes/fakulte_tab_panes.html', takes_context=True)
def render_fakulte_tab_panes(context, fakulte_sayfasi=None):
    if fakulte_sayfasi:
        fakulte_adi = fakulte_sayfasi.get_localized('fakulte_adi')
        ek_yoneticiler = [
            {
                'ad_soyad': y.ad_soyad,
                'gorev': y.get_localized('gorev'),
                'eposta': y.eposta,
                'telefon': y.telefon,
                'fotograf': y.fotograf,
                'ozgecmis_url': y.ozgecmis_url,
            }
            for y in fakulte_sayfasi.ek_yoneticiler.filter(aktif=True)
        ]
        ek_sekmeler = [
            {
                'id': f'ek_{sek.id}',
                'baslik': sek.get_localized('baslik'),
                'alt_baslik': sek.get_localized('alt_baslik'),
                'ikon': sek.ikon or 'fas fa-layer-group',
                'icerik': sek.get_localized('icerik'),
            }
            for sek in fakulte_sayfasi.ek_sekmeler.filter(aktif=True)
        ]
        bolum_kartlari = [
            {
                'ad': k.get_localized('ad'),
                'kisa_kod': k.kisa_kod,
                'ikon': k.ikon or 'fas fa-graduation-cap',
                'program_turu': k.get_localized('program_turu', _('Lisans Derecesi')),
                'egitim_dili': k.get_localized('egitim_dili', _('Türkçe')),
                'egitim_suresi': k.get_localized('egitim_suresi', _('4 Yıl')),
                'aciklama': k.get_localized('aciklama'),
                'detay_url': k.detay_url,
            }
            for k in fakulte_sayfasi.bolum_kartlari.filter(aktif=True)
        ]
        stats = []
        if fakulte_sayfasi.istatistikleri_goster:
            stat_specs = [
                (fakulte_sayfasi.get_localized('istatistik_1_baslik', _('Toplam Öğrenci')), fakulte_sayfasi.ogrenci_sayisi, 'fas fa-users'),
                (fakulte_sayfasi.get_localized('istatistik_2_baslik', _('Akademik Kadro')), fakulte_sayfasi.akademik_kadro_sayisi, 'fas fa-chalkboard-teacher'),
                (fakulte_sayfasi.get_localized('istatistik_3_baslik', _('Uluslararası Anlaşma')), fakulte_sayfasi.uluslararasi_anlasma_sayisi, 'fas fa-handshake'),
                (fakulte_sayfasi.get_localized('istatistik_4_baslik', _('Mezun İstihdam Oranı')), fakulte_sayfasi.mezun_istihdam_orani, 'fas fa-briefcase'),
            ]
            for lbl, val, ico in stat_specs:
                if val and str(val).strip():
                    stats.append({'label': lbl, 'value': str(val).strip(), 'icon': ico})
        data = {
            'exists': True,
            'show_bolumler': fakulte_sayfasi.bolumler_sekmesi_goster,
            'fakulte_adi': fakulte_adi,
            'bolumler_baslik': fakulte_sayfasi.get_localized('bolumler_baslik', _('Bölümler')),
            'bolumler_alt_baslik': fakulte_sayfasi.get_localized('bolumler_alt_baslik') or f"{fakulte_adi} {_('bünyesinde yer alan bölümler hakkında detaylı bilgi')}",
            'bolumler_giris_icerik': fakulte_sayfasi.get_localized('bolumler_giris_icerik'),
            'bolumler_liste_baslik': fakulte_sayfasi.get_localized('bolumler_liste_baslik', _('Lisans Programları')),
            'bolumler_liste_aciklama': fakulte_sayfasi.get_localized('bolumler_liste_aciklama'),
            'bolum_kartlari': bolum_kartlari,
            'stats': stats,
            'tarihce_baslik': fakulte_sayfasi.get_localized('tarihce_baslik', _('Tarihçe')),
            'tarihce_alt_baslik': fakulte_sayfasi.get_localized('tarihce_alt_baslik') or f"{fakulte_adi} {_('Tarihçesi')}",
            'tarihce_icerik': fakulte_sayfasi.get_localized('tarihce_icerik'),
            'mv_baslik': fakulte_sayfasi.get_localized('misyon_vizyon_baslik', _('Misyon & Vizyon')),
            'mv_alt_baslik': fakulte_sayfasi.get_localized('misyon_vizyon_alt_baslik') or f"{fakulte_adi} {_('Misyon & Vizyonu')}",
            'mv_giris': fakulte_sayfasi.get_localized('misyon_vizyon_giris'),
            'misyon_icerik': fakulte_sayfasi.get_localized('misyon_icerik'),
            'vizyon_icerik': fakulte_sayfasi.get_localized('vizyon_icerik'),
            'temel_degerler_icerik': fakulte_sayfasi.get_localized('temel_degerler_icerik'),
            'mesaj_baslik': fakulte_sayfasi.get_localized('mesaj_sekme_adi', _('Dekan Mesajı')),
            'mesaj_alt_baslik': fakulte_sayfasi.get_localized('mesaj_alt_baslik'),
            'yonetici_unvan_ad': fakulte_sayfasi.yonetici_unvan_ad,
            'yonetici_gorevi': fakulte_sayfasi.get_localized('yonetici_gorevi'),
            'yonetici_unvan_rozet': fakulte_sayfasi.get_localized('yonetici_unvan_rozet'),
            'yonetici_eposta': fakulte_sayfasi.yonetici_eposta,
            'yonetici_telefon': fakulte_sayfasi.yonetici_telefon,
            'ziyaret_saatleri': fakulte_sayfasi.ziyaret_saatleri,
            'yonetici_fotografi': fakulte_sayfasi.yonetici_fotografi,
            'dekan_mesaji': fakulte_sayfasi.get_localized('dekan_mesaji'),
            'ek_yoneticiler': ek_yoneticiler,
            'ek_sekmeler': ek_sekmeler,
        }
    else:
        data = {
            'exists': False,
            'show_bolumler': True,
            'fakulte_adi': '',
            'bolumler_baslik': _('Bölümler'),
            'bolumler_alt_baslik': '',
            'bolumler_giris_icerik': '',
            'bolumler_liste_baslik': _('Lisans Programları'),
            'bolumler_liste_aciklama': '',
            'bolum_kartlari': [],
            'stats': [],
            'tarihce_baslik': _('Tarihçe'),
            'tarihce_alt_baslik': '',
            'tarihce_icerik': '',
            'mv_baslik': _('Misyon & Vizyon'),
            'mv_alt_baslik': '',
            'mv_giris': '',
            'misyon_icerik': '',
            'vizyon_icerik': '',
            'temel_degerler_icerik': '',
            'mesaj_baslik': _('Dekan Mesajı'),
            'mesaj_alt_baslik': '',
            'yonetici_unvan_ad': '',
            'yonetici_gorevi': '',
            'yonetici_unvan_rozet': '',
            'yonetici_eposta': '',
            'yonetici_telefon': '',
            'ziyaret_saatleri': '',
            'yonetici_fotografi': None,
            'dekan_mesaji': '',
            'ek_yoneticiler': [],
            'ek_sekmeler': [],
        }

    return {'f': data, 'fakulte_obj': fakulte_sayfasi}
