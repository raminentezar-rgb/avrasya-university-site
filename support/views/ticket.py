from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from support.models import Category, Department, Ticket
from support.services.notifier import notify_department, notify_requester_created
from support.services.uploads import validate_attachment


def create_ticket(request):
    departments = Department.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')

    is_authenticated = request.user.is_authenticated
    default_name = (request.user.get_full_name() or request.user.username) if is_authenticated else ''
    default_email = (request.user.email or '') if is_authenticated else ''

    form_data = {
        'guest_name': default_name,
        'guest_email': default_email,
        'guest_phone': '',
        'subject': (request.GET.get('subject') or '').strip(),
        'message': '',
        'department': (request.GET.get('department') or '').strip(),
        'category': '',
        'priority': 'medium',
    }

    if request.method == 'POST':
        guest_name = (request.POST.get('guest_name') or default_name or '').strip()
        guest_email = (request.POST.get('guest_email') or default_email or '').strip()
        guest_phone = (request.POST.get('guest_phone') or '').strip()
        subject = (request.POST.get('subject') or '').strip()
        message_text = (request.POST.get('message') or '').strip()
        dept_raw = (request.POST.get('department') or '').strip()
        cat_raw = (request.POST.get('category') or '').strip()
        priority = (request.POST.get('priority') or 'medium').strip()
        attachment = request.FILES.get('attachment')

        form_data = {
            'guest_name': guest_name,
            'guest_email': guest_email,
            'guest_phone': guest_phone,
            'subject': subject,
            'message': message_text,
            'department': dept_raw,
            'category': cat_raw,
            'priority': priority,
        }

        if priority not in {'low', 'medium', 'high'}:
            priority = 'medium'

        department = None
        if dept_raw.isdigit():
            department = Department.objects.filter(id=int(dept_raw)).first()

        category = None
        if cat_raw.isdigit() and department:
            category = Category.objects.filter(id=int(cat_raw), department=department).first()

        email_valid = True
        if not is_authenticated or guest_email:
            try:
                validate_email(guest_email)
            except ValidationError:
                email_valid = False

        attachment_ok, attachment_err = validate_attachment(attachment)

        if not is_authenticated and not guest_name:
            messages.error(request, "Lütfen adınızı ve soyadınızı giriniz.")
        elif not is_authenticated and (not guest_email or not email_valid):
            messages.error(request, "Lütfen geçerli bir e-posta adresi giriniz.")
        elif guest_email and not email_valid:
            messages.error(request, "Lütfen geçerli bir e-posta adresi giriniz.")
        elif not department:
            messages.error(request, "Lütfen geçerli bir ilgili birim seçiniz.")
        elif not subject:
            messages.error(request, "Lütfen konu başlığını giriniz.")
        elif not message_text:
            messages.error(request, "Lütfen sorun veya soru detayını giriniz.")
        elif department.category_set.exists() and not category:
            messages.error(request, "Lütfen seçilen birime ait bir kategori seçiniz.")
        elif not attachment_ok:
            messages.error(request, attachment_err)
        else:
            ticket = Ticket.objects.create(
                user=request.user if is_authenticated else None,
                guest_name='' if is_authenticated else guest_name[:150],
                guest_email=guest_email if not is_authenticated else ('' if request.user.email else guest_email),
                guest_phone=guest_phone[:30],
                subject=subject[:255],
                message=message_text,
                department=department,
                category=category,
                priority=priority,
                attachment=attachment,
            )

            verified = list(request.session.get('verified_ticket_codes', []))
            if ticket.tracking_code and ticket.tracking_code not in verified:
                verified.append(ticket.tracking_code)
                request.session['verified_ticket_codes'] = verified

            notify_department(ticket)
            notify_requester_created(ticket)
            messages.success(
                request,
                f"Destek talebiniz oluşturuldu. Takip kodunuz: {ticket.tracking_code}",
            )
            return redirect('support:ticket_detail', ticket_id=ticket.id)

    return render(request, 'support/ticket_create.html', {
        'departments': departments,
        'categories': categories,
        'form_data': form_data,
    })
