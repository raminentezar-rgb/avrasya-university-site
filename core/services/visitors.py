import datetime
import hashlib
import logging
import os
import re
import threading
import time

from django.conf import settings

try:
    import redis
except ImportError:  # pragma: no cover
    redis = None

logger = logging.getLogger(__name__)

WINDOW_SECONDS = 300  # 5-minute active visitor sliding window
_ZSET_KEY = "avrasya:online_visitors:zset"
_PEAK_KEY_PREFIX = "avrasya:online_visitors:peak:"
_REDIS_BACKOFF_SECONDS = 60

_IGNORED_PREFIXES = (
    "/static/",
    "/media/",
    "/favicon.ico",
    "/robots.txt",
    "/sitemap.xml",
    "/api/",
    "/i18n/",
    "/set-language/",
    "/ckeditor/",
    "/ws/",
    "/admin/",
    "/avrasya-yonetim-paneli-2026/",
    "/chat/poll/",
    "/support/ajax/",
    "/support/api/",
)

_IGNORED_EXTENSIONS = (
    ".css", ".js", ".map", ".png", ".jpg", ".jpeg", ".gif", ".webp",
    ".svg", ".ico", ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".webm",
    ".pdf", ".xml", ".txt", ".json",
)

_BOT_USER_AGENT_RE = re.compile(
    r"(bot|crawl|spider|slurp|mediapartners|bingpreview|facebookexternalhit|"
    r"whatsapp|telegrambot|discordbot|linkedinbot|pinterest|semrush|ahrefs|"
    r"mj12bot|dotbot|petalbot|yandex|baiduspider|duckduckbot|applebot|"
    r"python-requests|python-urllib|httpx|aiohttp|curl|wget|scrapy|postman|"
    r"insomnia|headlesschrome|lighthouse|pagespeed|gtmetrix|pingdom|uptimerobot|"
    r"statuscake|monitoring)",
    re.IGNORECASE,
)

_MEM_LOCK = threading.Lock()
_MEM_VISITORS: dict[str, float] = {}
_MEM_PEAKS: dict[str, int] = {}

_REDIS_LOCK = threading.Lock()
_REDIS_CLIENT = None
_REDIS_RETRY_AT = 0.0


def _get_redis_client():
    """Return a shared Redis client if Redis is reachable, else None with backoff."""
    global _REDIS_CLIENT, _REDIS_RETRY_AT
    if redis is None:
        return None
    if os.environ.get("USE_REDIS_VISITORS", "").lower() == "false":
        return None

    now = time.monotonic()
    with _REDIS_LOCK:
        if now < _REDIS_RETRY_AT:
            return None
        if _REDIS_CLIENT is not None:
            return _REDIS_CLIENT
        redis_url = getattr(settings, "REDIS_URL", None) or os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")
        try:
            client = redis.Redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=0.3,
                socket_timeout=0.3,
            )
            client.ping()
            _REDIS_CLIENT = client
            return _REDIS_CLIENT
        except Exception:
            _REDIS_CLIENT = None
            _REDIS_RETRY_AT = now + _REDIS_BACKOFF_SECONDS
            return None


def _invalidate_redis_client():
    global _REDIS_CLIENT, _REDIS_RETRY_AT
    with _REDIS_LOCK:
        _REDIS_CLIENT = None
        _REDIS_RETRY_AT = time.monotonic() + _REDIS_BACKOFF_SECONDS


def _extract_client_ip(request) -> str:
    xff = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def should_track_request(request) -> bool:
    """Return True for genuine page navigation requests worth counting."""
    if request.method not in ("GET", "HEAD"):
        return False

    path = (request.path_info or request.path or "/").lower()
    if any(path.startswith(prefix) for prefix in _IGNORED_PREFIXES):
        return False
    if path != "/" and path.endswith(_IGNORED_EXTENSIONS):
        return False

    admin_prefix = "/" + os.environ.get("DJANGO_ADMIN_URL", "avrasya-yonetim-paneli-2026/").lstrip("/").lower()
    if admin_prefix != "/" and path.startswith(admin_prefix):
        return False

    purpose = (
        request.META.get("HTTP_SEC_PURPOSE", "") or request.META.get("HTTP_PURPOSE", "")
    ).lower()
    if "prefetch" in purpose or "prerender" in purpose:
        return False

    if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
        return False

    user_agent = request.META.get("HTTP_USER_AGENT", "")
    if user_agent and _BOT_USER_AGENT_RE.search(user_agent):
        return False

    return True


def _extract_visitor_id(request) -> str:
    """Compute an anonymized visitor token with zero database writes."""
    user = getattr(request, "user", None)
    if user is not None and getattr(user, "is_authenticated", False):
        return f"u:{user.pk}"

    session = getattr(request, "session", None)
    if session is not None and getattr(session, "session_key", None):
        return f"s:{session.session_key}"

    ip = _extract_client_ip(request)
    ua = request.META.get("HTTP_USER_AGENT", "")
    secret_salt = (getattr(settings, "SECRET_KEY", "") or "")[:16]
    digest = hashlib.sha256(f"{ip}|{ua}|{secret_salt}".encode("utf-8", "ignore")).hexdigest()[:24]
    return f"a:{digest}"


def _update_mem_peak(today_key: str, count: int) -> int:
    prev = _MEM_PEAKS.get(today_key, 0)
    if count > prev:
        _MEM_PEAKS[today_key] = count
        if len(_MEM_PEAKS) > 7:
            for old_key in sorted(_MEM_PEAKS.keys())[:-7]:
                _MEM_PEAKS.pop(old_key, None)
        return count
    return prev


def record_visitor(request) -> int:
    """Record the visitor in Redis (or memory fallback) and return active visitor count."""
    if not should_track_request(request):
        return get_online_visitors_count()

    visitor_id = _extract_visitor_id(request)
    now = time.time()
    cutoff = now - WINDOW_SECONDS
    today = datetime.date.today().isoformat()

    client = _get_redis_client()
    if client is not None:
        try:
            pipe = client.pipeline()
            pipe.zadd(_ZSET_KEY, {visitor_id: now})
            pipe.zremrangebyscore(_ZSET_KEY, "-inf", cutoff)
            pipe.expire(_ZSET_KEY, WINDOW_SECONDS + 60)
            pipe.zcard(_ZSET_KEY)
            _, _, _, count = pipe.execute()
            count = int(count)
            peak_key = f"{_PEAK_KEY_PREFIX}{today}"
            current_peak = int(client.get(peak_key) or 0)
            if count > current_peak:
                client.set(peak_key, count, ex=86400 * 3)
            return count
        except Exception:
            _invalidate_redis_client()

    with _MEM_LOCK:
        _MEM_VISITORS[visitor_id] = now
        expired = [vid for vid, ts in _MEM_VISITORS.items() if ts < cutoff]
        for vid in expired:
            del _MEM_VISITORS[vid]
        count = len(_MEM_VISITORS)
        _update_mem_peak(today, count)
        return count


def get_online_visitors_count() -> int:
    """Return active visitors within the 5-minute sliding window."""
    return get_visitor_stats()["online_count"]


def get_visitor_stats() -> dict:
    """Return real-time online count, today's concurrent peak, window length, and storage backend."""
    now = time.time()
    cutoff = now - WINDOW_SECONDS
    today = datetime.date.today().isoformat()

    client = _get_redis_client()
    if client is not None:
        try:
            pipe = client.pipeline()
            pipe.zremrangebyscore(_ZSET_KEY, "-inf", cutoff)
            pipe.zcard(_ZSET_KEY)
            pipe.get(f"{_PEAK_KEY_PREFIX}{today}")
            _, count, raw_peak = pipe.execute()
            count = int(count)
            peak_today = max(count, int(raw_peak or 0))
            return {
                "online_count": count,
                "peak_today": peak_today,
                "window_minutes": WINDOW_SECONDS // 60,
                "backend": "redis",
            }
        except Exception:
            _invalidate_redis_client()

    with _MEM_LOCK:
        expired = [vid for vid, ts in _MEM_VISITORS.items() if ts < cutoff]
        for vid in expired:
            del _MEM_VISITORS[vid]
        count = len(_MEM_VISITORS)
        peak_today = _update_mem_peak(today, count)

    return {
        "online_count": count,
        "peak_today": peak_today,
        "window_minutes": WINDOW_SECONDS // 60,
        "backend": "memory",
    }
