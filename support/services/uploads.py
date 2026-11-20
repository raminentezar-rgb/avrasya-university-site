import os

MAX_ATTACHMENT_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_ATTACHMENT_EXTENSIONS = {
    '.pdf', '.doc', '.docx', '.xls', '.xlsx',
    '.txt', '.png', '.jpg', '.jpeg', '.webp',
}


def validate_attachment(uploaded_file, extra_extensions=None):
    """Validate uploaded support or chat attachment size and extension."""
    if not uploaded_file:
        return True, None
    if uploaded_file.size > MAX_ATTACHMENT_SIZE:
        return False, "Dosya boyutu en fazla 10 MB olabilir."
    allowed = ALLOWED_ATTACHMENT_EXTENSIONS
    if extra_extensions:
        allowed = allowed | set(extra_extensions)
    ext = os.path.splitext(uploaded_file.name or '')[1].lower()
    if ext not in allowed:
        return False, "İzin verilmeyen dosya uzantısı."
    return True, None
