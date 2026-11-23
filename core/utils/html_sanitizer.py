import html
from html.parser import HTMLParser
import re


ALLOWED_TAGS = {
    'a', 'abbr', 'b', 'blockquote', 'br', 'caption', 'code', 'col', 'colgroup',
    'dd', 'del', 'div', 'dl', 'dt', 'em', 'figcaption', 'figure', 'h1', 'h2',
    'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'ins', 'li', 'ol', 'p', 'pre',
    's', 'small', 'span', 'strong', 'sub', 'sup', 'table', 'tbody', 'td',
    'tfoot', 'th', 'thead', 'tr', 'u', 'ul',
}
VOID_TAGS = {'br', 'hr', 'img', 'col'}
STRIP_WITH_CONTENT_TAGS = {'script', 'style', 'object', 'embed', 'applet', 'noscript'}
SAFE_URI_RE = re.compile(r'^(?:https?://|mailto:|tel:|/|#)', re.IGNORECASE)
ALLOWED_ATTRS = {
    '*': {'class', 'id', 'title', 'dir', 'lang', 'style'},
    'a': {'href', 'target', 'rel'},
    'img': {'src', 'alt', 'width', 'height', 'loading'},
    'td': {'colspan', 'rowspan', 'align', 'valign'},
    'th': {'colspan', 'rowspan', 'scope', 'align', 'valign'},
    'table': {'border', 'cellpadding', 'cellspacing', 'width'},
}
DANGEROUS_CSS_RE = re.compile(r'(?:expression\s*\(|javascript:|vbscript:|url\s*\(\s*["\']?\s*javascript:)', re.IGNORECASE)


class _SafeHTMLSanitizer(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        tag_l = tag.lower()
        if tag_l in STRIP_WITH_CONTENT_TAGS:
            self._skip_depth += 1
            return
        if self._skip_depth > 0 or tag_l not in ALLOWED_TAGS:
            return
        allowed = ALLOWED_ATTRS['*'] | ALLOWED_ATTRS.get(tag_l, set())
        clean_attrs = []
        has_target_blank = False
        has_rel = False
        for k, v in attrs:
            kl = (k or '').lower()
            if kl.startswith('on') or kl not in allowed:
                continue
            val = v or ''
            if kl in ('href', 'src'):
                v_strip = val.strip()
                if not v_strip or not SAFE_URI_RE.match(v_strip):
                    continue
            if kl == 'style' and DANGEROUS_CSS_RE.search(val):
                continue
            if kl == 'target' and val.strip().lower() == '_blank':
                has_target_blank = True
            if kl == 'rel':
                has_rel = True
            clean_attrs.append(f' {kl}="{html.escape(val, quote=True)}"')
        if tag_l == 'a' and has_target_blank and not has_rel:
            clean_attrs.append(' rel="noopener noreferrer"')
        self.out.append(f'<{tag_l}{"".join(clean_attrs)}>')

    def handle_endtag(self, tag):
        tag_l = tag.lower()
        if tag_l in STRIP_WITH_CONTENT_TAGS:
            if self._skip_depth > 0:
                self._skip_depth -= 1
            return
        if self._skip_depth > 0 or tag_l not in ALLOWED_TAGS or tag_l in VOID_TAGS:
            return
        self.out.append(f'</{tag_l}>')

    def handle_data(self, data):
        if self._skip_depth == 0:
            self.out.append(html.escape(data, quote=False))

    def handle_entityref(self, name):
        if self._skip_depth == 0:
            self.out.append(f'&{name};')

    def handle_charref(self, name):
        if self._skip_depth == 0:
            self.out.append(f'&#{name};')


def sanitize_rich_html(raw_html):
    """Strip scripts, event handlers, and unsafe URIs from rich HTML while keeping CKEditor formatting."""
    if not raw_html:
        return ''
    parser = _SafeHTMLSanitizer()
    parser.feed(str(raw_html))
    parser.close()
    return ''.join(parser.out)
