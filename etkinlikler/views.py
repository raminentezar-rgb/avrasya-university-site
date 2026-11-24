import logging
import re

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.db import transaction
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST

from .models import Etkinlik, EtkinlikBildirimAboneligi, EtkinlikKayit

logger = logging.getLogger(__name__)


def _clean_text(val: str, max_len: int = 200) -> str:
    return re.sub(r'[\r\n]+', ' ', str(val or '')).strip()[:max_len]


def _client_ip(request) -> str:
    xff = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


def _is_rate_limited(bucket: str, ip: str, limit: int = 10, window: int = 600) -> bool:
    key = f"etkinlikler:rl:{bucket}:{ip}"
    count = cache.get(key, 0)
    if count >= limit:
        return True
    if count == 0:
        cache.set(key, 1, window)
    else:
        try:
            cache.incr(key)
        except ValueError:
            cache.set(key, count + 1, window)
    return False


def _ics_escape(val: str) -> str:
    text = str(val or '').replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,')
    return re.sub(r'\r?\n', '\\n', text)


def etkinlik_listesi(request):
    search_query = request.GET.get('q', '').strip()
    tur_filter = request.GET.get('tur', '').strip()
    birim_filter = request.GET.get('birim', '').strip()
    ucret_filter = request.GET.get('ucret', '').strip()
    kayit_filter = request.GET.get('kayit', '').strip()
    sort_param = request.GET.get('sort', 'newest')

    etkinlikler = (
        Etkinlik.objects.filter(yayinda=True)
        .annotate(_aktif_kayit_sayisi=Count('kayitlar', filter=~Q(kayitlar__durum='iptal'), distinct=True))
        .prefetch_related('gorseller', 'dosyalar', 'konusmacilar')
    )

    if search_query:
        etkinlikler = etkinlikler.filter(
            Q(baslik__icontains=search_query)
            | Q(kisa_aciklama__icontains=search_query)
            | Q(detayli_aciklama__icontains=search_query)
            | Q(yer__icontains=search_query)
            | Q(duzenleyen__icontains=search_query)
            | Q(etkinlik_turu__icontains=search_query)
            | Q(konusmacilar__ad_soyad__icontains=search_query)
        ).distinct()

    valid_turler = dict(Etkinlik.ETKINLIK_TURU_CHOICES)
    if tur_filter in valid_turler:
        etkinlikler = etkinlikler.filter(etkinlik_turu=tur_filter)
    else:
        tur_filter = ''

    valid_birimler = dict(Etkinlik.BIRIM_CHOICES)
    if birim_filter in valid_birimler:
        etkinlikler = etkinlikler.filter(fakulte=birim_filter)
    else:
        birim_filter = ''

    if ucret_filter == 'ucretsiz':
        etkinlikler = etkinlikler.filter(ucretli=False)
    elif ucret_filter == 'ucretli':
        etkinlikler = etkinlikler.filter(ucretli=True)
    else:
        ucret_filter = ''

    if kayit_filter == 'gerekiyor':
        etkinlikler = etkinlikler.filter(kayit_gerekiyor=True)
    elif kayit_filter == 'acik':
        etkinlikler = etkinlikler.filter(kayit_gerekiyor=False)
    else:
        kayit_filter = ''

    simdi = timezone.now()
    gelecek_etkinlikler = etkinlikler.filter(baslangic_tarihi__gte=simdi)
    gecmis_qs = etkinlikler.filter(baslangic_tarihi__lt=simdi)

    if sort_param == 'oldest':
        gelecek_etkinlikler = gelecek_etkinlikler.order_by('-baslangic_tarihi')
        gecmis_qs = gecmis_qs.order_by('baslangic_tarihi')
    elif sort_param == 'upcoming':
        gelecek_etkinlikler = gelecek_etkinlikler.order_by('baslangic_tarihi')
        gecmis_qs = gecmis_qs.order_by('-baslangic_tarihi')
    else:
        sort_param = 'newest'
        gelecek_etkinlikler = gelecek_etkinlikler.order_by('baslangic_tarihi')
        gecmis_qs = gecmis_qs.order_by('-baslangic_tarihi')

    paginator = Paginator(gecmis_qs, 9)
    gecmis_page_obj = paginator.get_page(request.GET.get('page'))

    has_active_filters = bool(search_query or tur_filter or birim_filter or ucret_filter or kayit_filter)

    return render(request, 'etkinlikler/list.html', {
        'gelecek_etkinlikler': gelecek_etkinlikler,
        'gecmis_etkinlikler': gecmis_page_obj,
        'gecmis_total_count': paginator.count,
        'search_query': search_query,
        'tur_filter': tur_filter,
        'birim_filter': birim_filter,
        'ucret_filter': ucret_filter,
        'kayit_filter': kayit_filter,
        'sort_param': sort_param,
        'has_active_filters': has_active_filters,
        'etkinlik_turu_choices': Etkinlik.ETKINLIK_TURU_CHOICES,
        'birim_choices': Etkinlik.BIRIM_CHOICES,
    })


def etkinlik_detay(request, slug):
    etkinlik = get_object_or_404(
        Etkinlik.objects.annotate(
            _aktif_kayit_sayisi=Count('kayitlar', filter=~Q(kayitlar__durum='iptal'), distinct=True)
        ).prefetch_related('gorseller', 'dosyalar', 'konusmacilar'),
        slug=slug,
        yayinda=True,
    )
    return render(request, 'etkinlikler/detail.html', {
        'etkinlik': etkinlik,
        'birim_choices': Etkinlik.BIRIM_CHOICES,
    })


def yaklasan_etkinlikler(request):
    """Yaklaşan etkinlikler (7 gün içinde)."""
    search_query = request.GET.get('q', '').strip()

    yedi_gun_sonra = timezone.now() + timezone.timedelta(days=7)
    etkinlikler = (
        Etkinlik.objects.filter(
            yayinda=True,
            baslangic_tarihi__range=[timezone.now(), yedi_gun_sonra],
        )
        .annotate(_aktif_kayit_sayisi=Count('kayitlar', filter=~Q(kayitlar__durum='iptal'), distinct=True))
        .prefetch_related('gorseller', 'dosyalar', 'konusmacilar')
    )

    if search_query:
        etkinlikler = etkinlikler.filter(
            Q(baslik__icontains=search_query)
            | Q(kisa_aciklama__icontains=search_query)
            | Q(detayli_aciklama__icontains=search_query)
            | Q(yer__icontains=search_query)
            | Q(duzenleyen__icontains=search_query)
            | Q(etkinlik_turu__icontains=search_query)
        )

    etkinlikler = etkinlikler.order_by('baslangic_tarihi')
    kayit_gereken_etkinlikler = etkinlikler.filter(kayit_gerekiyor=True).count()
    farkli_mekanlar = etkinlikler.values('yer').distinct().count()

    return render(request, 'etkinlikler/yaklasan.html', {
        'etkinlikler': etkinlikler,
        'search_query': search_query,
        'kayit_gereken_etkinlikler': kayit_gereken_etkinlikler,
        'farkli_mekanlar': farkli_mekanlar,
        'etkinlik_turu_choices': Etkinlik.ETKINLIK_TURU_CHOICES,
    })


def etkinlik_takvim_ics(request, slug):
    """Generate RFC 5545 .ics calendar file for Apple/Outlook/Google Calendar."""
    etkinlik = get_object_or_404(Etkinlik, slug=slug, yayinda=True)
    start_utc = timezone.localtime(etkinlik.baslangic_tarihi, timezone.UTC)
    end_dt = etkinlik.bitis_tarihi or (etkinlik.baslangic_tarihi + timezone.timedelta(hours=2))
    end_utc = timezone.localtime(end_dt, timezone.UTC)
    now_utc = timezone.localtime(timezone.now(), timezone.UTC)

    description = strip_tags(etkinlik.get_ozet or etkinlik.detayli_aciklama or '').strip()[:800]
    event_url = request.build_absolute_uri(etkinlik.get_absolute_url())
    safe_filename = re.sub(r'[^a-zA-Z0-9_-]', '-', etkinlik.slug)[:80] or 'etkinlik'

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Avrasya Universitesi//Etkinlikler//TR",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "BEGIN:VEVENT",
        f"UID:etkinlik-{etkinlik.pk}@avrasya.edu.tr",
        f"DTSTAMP:{now_utc.strftime('%Y%m%dT%H%M%SZ')}",
        f"DTSTART:{start_utc.strftime('%Y%m%dT%H%M%SZ')}",
        f"DTEND:{end_utc.strftime('%Y%m%dT%H%M%SZ')}",
        f"SUMMARY:{_ics_escape(etkinlik.baslik)}",
        f"LOCATION:{_ics_escape(etkinlik.yer)}",
        f"DESCRIPTION:{_ics_escape(description)}",
        f"URL:{event_url}",
        "END:VEVENT",
        "END:VCALENDAR",
    ]
    response = HttpResponse("\r\n".join(lines) + "\r\n", content_type="text/calendar; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{safe_filename}.ics"'
    return response


@require_POST
def etkinlik_kayit_ol(request, slug):
    """Register an attendee for an event with concurrency-safe capacity enforcement."""
    ip = _client_ip(request)
    if _is_rate_limited("kayit", ip, limit=12, window=600):
        return JsonResponse(
            {"success": False, "error": "Çok fazla deneme yaptınız. Lütfen birkaç dakika sonra tekrar deneyiniz."},
            status=429,
        )

    ad_soyad = _clean_text(request.POST.get("ad_soyad"), 150)
    email = _clean_text(request.POST.get("email"), 150).lower()
    telefon = _clean_text(request.POST.get("telefon"), 30)
    ogrenci_no = _clean_text(request.POST.get("ogrenci_no"), 50)
    kurum_fakulte = _clean_text(request.POST.get("kurum_fakulte"), 150)
    notlar = str(request.POST.get("notlar") or "").strip()[:1000]

    if not ad_soyad or not email or not telefon:
        return JsonResponse(
            {"success": False, "error": "Lütfen ad soyad, e-posta ve telefon alanlarını eksiksiz doldurunuz."},
            status=400,
        )

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"success": False, "error": "Lütfen geçerli bir e-posta adresi giriniz."}, status=400)

    if len(re.sub(r'\D', '', telefon)) < 7:
        return JsonResponse({"success": False, "error": "Lütfen geçerli bir telefon numarası giriniz."}, status=400)

    with transaction.atomic():
        etkinlik = get_object_or_404(Etkinlik.objects.select_for_update(), slug=slug, yayinda=True)
        is_open, reason = etkinlik.kayit_durumu
        if not is_open:
            return JsonResponse({"success": False, "error": reason}, status=400)

        already = etkinlik.kayitlar.filter(email=email).exclude(durum='iptal').exists()
        if already:
            return JsonResponse(
                {"success": False, "error": "Bu e-posta adresi ile bu etkinliğe zaten aktif bir kaydınız bulunuyor."},
                status=409,
            )

        kayit = EtkinlikKayit.objects.create(
            etkinlik=etkinlik,
            ad_soyad=ad_soyad,
            email=email,
            telefon=telefon,
            ogrenci_no=ogrenci_no,
            kurum_fakulte=kurum_fakulte,
            notlar=notlar,
        )
        aktif_sayi = etkinlik.kayitlar.exclude(durum='iptal').count()
        kalan = max(0, etkinlik.kontenjan - aktif_sayi) if etkinlik.kontenjan is not None else None

    try:
        local_dt = timezone.localtime(etkinlik.baslangic_tarihi).strftime('%d.%m.%Y %H:%M')
        msg = EmailMessage(
            subject=f"Etkinlik Kayıt Onayı: {etkinlik.baslik}",
            body=(
                f"Sayın {ad_soyad},\n\n"
                f"\"{etkinlik.baslik}\" etkinliğine kaydınız başarıyla alınmıştır.\n\n"
                f"Kayıt Kodunuz: {kayit.kayit_kodu}\n"
                f"Tarih & Saat: {local_dt}\n"
                f"Yer: {etkinlik.yer}\n\n"
                f"Avrasya Üniversitesi"
            ),
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@avrasya.edu.tr'),
            to=[email],
        )
        msg.send(fail_silently=True)
    except Exception as exc:
        logger.warning("Etkinlik kayıt onay e-postası gönderilemedi: %s", exc)

    return JsonResponse({
        "success": True,
        "kayit_kodu": kayit.kayit_kodu,
        "ad_soyad": kayit.ad_soyad,
        "kalan_kontenjan": kalan,
        "aktif_kayit_sayisi": aktif_sayi,
        "message": f"Kaydınız başarıyla oluşturuldu. Kayıt kodunuz: {kayit.kayit_kodu}",
    })


@require_POST
def etkinlik_bildirim_abone(request):
    """Subscribe a visitor email to upcoming university event alerts."""
    ip = _client_ip(request)
    if _is_rate_limited("bildirim", ip, limit=10, window=600):
        return JsonResponse(
            {"success": False, "error": "Çok fazla deneme yaptınız. Lütfen biraz sonra tekrar deneyiniz."},
            status=429,
        )

    email = _clean_text(request.POST.get("email"), 150).lower()
    ad_soyad = _clean_text(request.POST.get("ad_soyad"), 150)
    tercih_turu = _clean_text(request.POST.get("tercih_turu"), 50)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"success": False, "error": "Lütfen geçerli bir e-posta adresi giriniz."}, status=400)

    valid_types = {k for k, _ in Etkinlik.ETKINLIK_TURU_CHOICES}
    if tercih_turu and tercih_turu not in valid_types:
        tercih_turu = ''

    abone, created = EtkinlikBildirimAboneligi.objects.get_or_create(
        email=email,
        defaults={
            "ad_soyad": ad_soyad,
            "tercih_turu": tercih_turu,
            "aktif": True,
        },
    )
    if not created:
        abone.aktif = True
        if ad_soyad:
            abone.ad_soyad = ad_soyad
        abone.tercih_turu = tercih_turu
        abone.save()

    return JsonResponse({
        "success": True,
        "created": created,
        "message": "Etkinlik bildirim aboneliğiniz başarıyla kaydedildi.",
    })


def etkinlik_bildirim_iptal(request, token):
    """Unsubscribe an email alert subscriber safely using their private token."""
    abone = get_object_or_404(EtkinlikBildirimAboneligi, iptal_token=token)
    if abone.aktif:
        abone.aktif = False
        abone.save(update_fields=['aktif'])
    messages.success(request, "Etkinlik e-posta bildirim aboneliğiniz iptal edilmiştir.")
    return redirect('etkinlikler:liste')
