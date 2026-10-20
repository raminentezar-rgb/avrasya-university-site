from django import template
from django.utils import timezone
from datetime import datetime, date

register = template.Library()

TR_MONTHS = {
    1: 'Ocak',
    2: 'Şubat',
    3: 'Mart',
    4: 'Nisan',
    5: 'Mayıs',
    6: 'Haziran',
    7: 'Temmuz',
    8: 'Ağustos',
    9: 'Eylül',
    10: 'Ekim',
    11: 'Kasım',
    12: 'Aralık',
}

TR_MONTHS_UPPER = {
    1: 'OCAK',
    2: 'ŞUBAT',
    3: 'MART',
    4: 'NİSAN',
    5: 'MAYIS',
    6: 'HAZİRAN',
    7: 'TEMMUZ',
    8: 'AĞUSTOS',
    9: 'EYLÜL',
    10: 'EKİM',
    11: 'KASIM',
    12: 'ARALIK',
}

TR_MONTHS_SHORT = {
    1: 'Oca',
    2: 'Şub',
    3: 'Mar',
    4: 'Nis',
    5: 'May',
    6: 'Haz',
    7: 'Tem',
    8: 'Ağu',
    9: 'Eyl',
    10: 'Eki',
    11: 'Kas',
    12: 'Ara',
}

TR_MONTHS_SHORT_UPPER = {
    1: 'OCA',
    2: 'ŞUB',
    3: 'MAR',
    4: 'NİS',
    5: 'MAY',
    6: 'HAZ',
    7: 'TEM',
    8: 'AĞU',
    9: 'EYL',
    10: 'EKİ',
    11: 'KAS',
    12: 'ARA',
}

TR_WEEKDAYS = {
    0: 'Pazartesi',
    1: 'Salı',
    2: 'Çarşamba',
    3: 'Perşembe',
    4: 'Cuma',
    5: 'Cumartesi',
    6: 'Pazar',
}

TR_WEEKDAYS_SHORT = {
    0: 'Pzt',
    1: 'Sal',
    2: 'Çar',
    3: 'Per',
    4: 'Cum',
    5: 'Cmt',
    6: 'Paz',
}


def _extract_datetime(value):
    """Datetime nesnesini ayrıştırır"""
    if value is None:
        return None
    if isinstance(value, (datetime, date)):
        return value
    if isinstance(value, str):
        # ISO veya standart tarih formatlarını dene
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S%z', '%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y'):
            try:
                return datetime.strptime(value.split('+')[0].strip(), fmt)
            except (ValueError, TypeError):
                continue
    return None


@register.filter(name='tr_month_box')
def tr_month_box(value):
    """
    Tarih kutusu (Square Date Badge) için büyük harfli Türkçe ay adı döner.
    Örnek: 23 Ekim 2026 -> 'EKİM'
    """
    dt = _extract_datetime(value)
    if not dt:
        return ''
    return TR_MONTHS_UPPER.get(dt.month, '')


@register.filter(name='tr_month')
def tr_month(value):
    """
    Türkçe ay adı döner.
    Örnek: 23 Ekim 2026 -> 'Ekim'
    """
    dt = _extract_datetime(value)
    if not dt:
        return ''
    return TR_MONTHS.get(dt.month, '')


@register.filter(name='tr_month_short')
def tr_month_short(value):
    """
    Kısa Türkçe ay adı döner.
    Örnek: 23 Ekim 2026 -> 'Eki'
    """
    dt = _extract_datetime(value)
    if not dt:
        return ''
    return TR_MONTHS_SHORT.get(dt.month, '')


@register.filter(name='tr_day')
def tr_day(value):
    """
    Günü iki basamaklı olarak döner.
    Örnek: 23 Ekim 2026 -> '23'
    """
    dt = _extract_datetime(value)
    if not dt:
        return ''
    return f"{dt.day:02d}" if dt.day < 10 else str(dt.day)


@register.filter(name='tr_year')
def tr_year(value):
    """
    Yılı döner.
    Örnek: 23 Ekim 2026 -> '2026'
    """
    dt = _extract_datetime(value)
    if not dt:
        return ''
    return str(dt.year)


@register.filter(name='tr_weekday')
def tr_weekday(value):
    """
    Türkçe gün adı döner.
    Örnek: Cuma
    """
    dt = _extract_datetime(value)
    if not dt:
        return ''
    return TR_WEEKDAYS.get(dt.weekday(), '')


@register.filter(name='tr_date')
def tr_date(value, format_type='full'):
    """
    Tarihi Türkçe formatında döner:
    - 'full' / 'long' -> 23 Ekim 2026
    - 'short' -> 23 Eki 2026
    - 'with_weekday' -> 23 Ekim 2026 Cuma
    - 'with_time' -> 23 Ekim 2026 • 11:00
    - 'time' -> 11:00
    """
    dt = _extract_datetime(value)
    if not dt:
        return ''

    day = dt.day
    year = dt.year
    month_name = TR_MONTHS.get(dt.month, '')
    month_short = TR_MONTHS_SHORT.get(dt.month, '')
    weekday_name = TR_WEEKDAYS.get(dt.weekday(), '')

    has_time = isinstance(dt, datetime) and (dt.hour != 0 or dt.minute != 0)
    time_str = f"{dt.hour:02d}:{dt.minute:02d}" if isinstance(dt, datetime) else ""

    if format_type in ('full', 'long'):
        return f"{day} {month_name} {year}"
    elif format_type == 'short':
        return f"{day} {month_short} {year}"
    elif format_type == 'with_weekday':
        return f"{day} {month_name} {year} {weekday_name}"
    elif format_type == 'with_time':
        if has_time:
            return f"{day} {month_name} {year} • {time_str}"
        return f"{day} {month_name} {year}"
    elif format_type == 'time':
        return time_str
    elif format_type == 'box':
        return TR_MONTHS_UPPER.get(dt.month, '')
    
    return f"{day} {month_name} {year}"
