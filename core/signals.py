from django.conf import settings
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_delete, post_save

_SEARCH_SIGNALS_CONNECTED = False


def clear_all_public_caches(**kwargs):
    """Invalidate search index, homepage context/fragments, and announcement statistics."""
    try:
        from support.services.search import clear_search_index
        clear_search_index()
    except Exception:
        pass

    cache.delete("duyurular:stats:v1")
    cache.delete("core:admin_dashboard_stats:v1")

    lang_codes = [code for code, _ in getattr(settings, "LANGUAGES", [("tr", "Turkish")])]
    for lang in lang_codes:
        cache.delete(f"core:homepage_context:v1:{lang}")
        for fragment_name in ("index_news", "index_announcements"):
            try:
                cache.delete(make_template_fragment_key(fragment_name, [lang]))
            except Exception:
                pass


def connect_cache_invalidation_signals():
    """Connect post_save/post_delete signals once for searchable and homepage models."""
    global _SEARCH_SIGNALS_CONNECTED
    if _SEARCH_SIGNALS_CONNECTED:
        return

    from django.apps import apps

    model_labels = (
        "news.News",
        "duyurular.Duyuru",
        "duyurular.Bolum",
        "etkinlikler.Etkinlik",
        "etkinlikler.EtkinlikGorsel",
        "etkinlikler.EtkinlikDosya",
        "etkinlikler.EtkinlikKonusmaci",
        "core.SliderItem",
        "core.QuestionAnswer",
        "support.FAQ",
        "support.KnowledgeBase",
        "support.ImportantLink",
        "support.Department",
        "akademik.FakulteSayfasi",
        "akademik.BolumSayfasi",
        "akademik.BolumAkademikKadroUyesi",
        "kalite_akreditasyon.BolumKalite",
    )

    for label in model_labels:
        try:
            model = apps.get_model(label)
        except LookupError:
            continue
        uid = f"avrasya_cache_invalidate_{label}"
        post_save.connect(clear_all_public_caches, sender=model, dispatch_uid=f"{uid}_save", weak=False)
        post_delete.connect(clear_all_public_caches, sender=model, dispatch_uid=f"{uid}_delete", weak=False)

    _SEARCH_SIGNALS_CONNECTED = True
