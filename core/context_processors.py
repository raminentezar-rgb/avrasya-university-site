import re
from django.conf import settings
from django.utils import translation

from .services.visitors import get_online_visitors_count

_NOINDEX_RE = re.compile(
    r"^/(?:[a-z]{2}/)?("
    r"adalet|accounts|chat|odeme/payment|"
    r"support/ticket|support/takip|support/taleplerim|"
    r"support/department|support/staff|"
    r"anasyafa|home|test|elements"
    r")(?:/|$)",
    re.IGNORECASE,
)


def is_noindex_path(path: str) -> bool:
    """Return True if a URL path should carry noindex directives."""
    return bool(_NOINDEX_RE.match(path or "/"))


def _strip_lang_prefix(path: str, lang_codes: list[str]) -> str:
    if not path or path == "/":
        return "/"
    for code in lang_codes:
        if path == f"/{code}" or path == f"/{code}/":
            return "/"
        if path.startswith(f"/{code}/"):
            return path[len(code) + 1:]
    return path


def _build_seo_urls(request):
    site_url = getattr(settings, "SITE_URL", "https://www.avrasya.edu.tr").rstrip("/")
    path = request.path or "/"
    default_lang = getattr(settings, "LANGUAGE_CODE", "tr")
    lang_codes = [code for code, _ in getattr(settings, "LANGUAGES", [("tr", "Turkish")])]
    bare_path = _strip_lang_prefix(path, lang_codes)
    if not bare_path.startswith("/"):
        bare_path = "/" + bare_path

    canonical_url = f"{site_url}{path}"
    hreflang_links = []
    for code in lang_codes:
        localized_path = bare_path if code == default_lang else f"/{code}{bare_path}"
        hreflang_links.append({
            "lang": code,
            "href": f"{site_url}{localized_path}",
        })
    hreflang_links.append({
        "lang": "x-default",
        "href": f"{site_url}{bare_path}",
    })
    return canonical_url, hreflang_links


def languages(request):
    code = translation.get_language() or getattr(settings, "LANGUAGE_CODE", "tr")
    canonical_url, hreflang_links = _build_seo_urls(request)
    noindex = is_noindex_path(request.path or "/")

    try:
        online_visitors = get_online_visitors_count()
    except Exception:
        online_visitors = 0

    return {
        "LANGUAGE_CODE": code,
        "CURRENT_LANG": code,
        "CURRENT_LANGUAGE": code,
        "LANGUAGE_BIDI": translation.get_language_bidi(),
        "CANONICAL_URL": canonical_url,
        "HREFLANG_LINKS": hreflang_links,
        "SEO_NOINDEX": noindex,
        "ONLINE_VISITORS_COUNT": online_visitors,
    }
