import json
import os
import re
import secrets
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.timesince import timesince
from support.services.uploads import validate_attachment
from .models import Message, Notification, SupportMessage, SupportThread, Thread


@login_required
def chat_index(request):
    """Render the main chat interface."""
    # Sadece staff ve professor rollerine izin ver
    if not hasattr(request.user, 'profile') or request.user.profile.role not in ['staff', 'professor']:
        messages.error(request, 'Bu sayfaya erişim yetkiniz yok.')
        return redirect('core:index')

    # Sadece geçerli diğer kullanıcısı olan thread'leri al
    threads = request.user.threads.filter(is_active=True).prefetch_related(
        'participants', 'messages'
    ).annotate(
        unread_count=Count('messages', filter=Q(messages__is_read=False) & ~Q(messages__sender=request.user))
    )
    
    # Get only staff and professor users for starting new chats (kullanıcıyı hariç tut)
    users = User.objects.exclude(id=request.user.id).filter(
        profile__role__in=['staff', 'professor']
    ).select_related('profile')
    
    # Prepare support threads for staff with last message preview
    support_threads = []
    if request.user.is_staff:
        support_qs = SupportThread.objects.filter(is_active=True).prefetch_related('support_messages').order_by('-updated_at')
        for s_thread in support_qs:
            msgs_list = list(s_thread.support_messages.all())
            s_thread.last_support_msg = msgs_list[-1] if msgs_list else None
            support_threads.append(s_thread)
    
    # Prepare threads data with other participant - sadece geçerli olanları ekle
    threads_with_participants = []
    requested_thread_id = request.GET.get('thread')
    selected_thread = None

    for thread in threads:
        other_user = thread.get_other_participant(request.user)
        if other_user:  # Sadece other_user varsa ekle
            entry = {
                'thread': thread,
                'other_user': other_user,
                'unread_count': getattr(thread, 'unread_count', 0),
                'last_message': thread.get_last_message()
            }
            threads_with_participants.append(entry)
            if requested_thread_id and str(thread.id) == str(requested_thread_id):
                selected_thread = entry

    first_valid_thread = selected_thread or (threads_with_participants[0] if threads_with_participants else None)
    
    context = {
        'threads_with_participants': threads_with_participants,
        'support_threads': support_threads,
        'users': users,
        'has_valid_threads': len(threads_with_participants) > 0,
        'first_valid_thread': first_valid_thread,
    }
    return render(request, 'chat/index.html', context)


@login_required
def thread_messages(request, thread_id):
    """Return JSON list of messages for a given thread."""
    # Sadece staff ve professor rollerine izin ver
    if not hasattr(request.user, 'profile') or request.user.profile.role not in ['staff', 'professor']:
        return JsonResponse({'error': 'Yetkisiz erişim'}, status=403)

    try:
        thread = request.user.threads.get(id=thread_id)
    except Thread.DoesNotExist:
        return JsonResponse({'error': 'Thread not found'}, status=404)
    
    # Get messages with pagination
    try:
        page = max(1, int(request.GET.get('page', 1)))
    except (TypeError, ValueError):
        page = 1
    page_size = 50
    start = (page - 1) * page_size
    end = start + page_size
    
    # Ø§Ø¨ØªØ¯Ø§ Ú©Ù„ Ú©ÙˆØ¦Ø±ÛŒ Ø±Ø§ Ù…ÛŒâ€ŒÚ¯ÛŒØ±ÛŒÙ…
    messages_query = thread.messages.select_related('sender').order_by('-created_at')
    
    # Ø§Ø¨ØªØ¯Ø§ Ù¾ÛŒØ§Ù…â€ŒÙ‡Ø§ÛŒ Ø®ÙˆØ§Ù†Ø¯Ù‡ Ù†Ø´Ø¯Ù‡ Ø±Ø§ Ø¢Ù¾Ø¯ÛŒØª Ù…ÛŒâ€ŒÚ©Ù†ÛŒÙ… (Ù‚Ø¨Ù„ Ø§Ø² Ø§Ø³Ù„Ø§ÛŒØ³)
    unread_messages = messages_query.filter(is_read=False).exclude(sender=request.user)
    unread_messages.update(is_read=True, is_delivered=True)
    
    # Ø³Ù¾Ø³ Ø§Ø³Ù„Ø§ÛŒØ³ Ø±Ø§ Ø§Ø¹Ù…Ø§Ù„ Ù…ÛŒâ€ŒÚ©Ù†ÛŒÙ…
    messages = list(messages_query[start:end])
    
    data = []
    for msg in messages:
        msg_data = {
            'id': msg.id,
            'sender_id': msg.sender.id,
            'sender_name': msg.sender.get_full_name() or msg.sender.username,
            'text': msg.text,
            'created_at': msg.created_at.strftime('%H:%M'),
            'created_at_full': msg.created_at.strftime('%Y-%m-%d %H:%M'),
            'file_url': msg.file.url if msg.file else None,
            'file_name': msg.file.name.split('/')[-1] if msg.file else None,
            'file_size': msg.file.size if msg.file else None,
            'is_read': msg.is_read,
            'is_sent': msg.sender == request.user,
        }
        data.append(msg_data)
    
    # Reverse to show in chronological order
    data.reverse()
    
    other_user = thread.get_other_participant(request.user)
    
    return JsonResponse({
        'messages': data,
        'has_more': messages_query.count() > end,
        'thread_id': thread_id,
        'other_user': {
            'id': other_user.id if other_user else None,
            'name': other_user.get_full_name() or other_user.username if other_user else 'Unknown',
        }
    })


@login_required
def send_message(request):
    """AJAX endpoint to send a message to a thread. (With notifications)"""
    # Sadece staff ve professor rollerine izin ver
    if not hasattr(request.user, 'profile') or request.user.profile.role not in ['staff', 'professor']:
        return JsonResponse({'error': 'Yetkisiz erişim'}, status=403)

    if request.method == 'POST':
        thread_id = request.POST.get('thread_id')
        text = request.POST.get('text', '').strip()
        file = request.FILES.get('file')
        temp_id = request.POST.get('temp_id')

        try:
            thread = request.user.threads.get(id=thread_id)
        except Thread.DoesNotExist:
            return JsonResponse({'error': 'Thread not found'}, status=404)

        if file:
            file_ok, file_err = validate_attachment(file, extra_extensions={'.zip'})
            if not file_ok:
                return JsonResponse({'error': file_err}, status=400)

        if text or file:
            msg = Message.objects.create(
                thread=thread,
                sender=request.user,
                text=text,
                file=file
            )
            
            # ارسال نوتیفیکیشن به سایر شرکت‌کنندگان
            other_users = thread.participants.exclude(id=request.user.id)
            for user in other_users:
                if text:
                    Notification.objects.create(
                        user=user,
                        notification_type='message',
                        title=f'Yeni mesaj: {request.user.get_full_name() or request.user.username}',
                        message=text[:100] + '...' if len(text) > 100 else text,
                        thread_id=thread.id,
                        sender_id=request.user.id
                    )
                elif file:
                    Notification.objects.create(
                        user=user,
                        notification_type='message',
                        title=f'Yeni dosya: {request.user.get_full_name() or request.user.username}',
                        message='Bir dosya gönderdi',
                        thread_id=thread.id,
                        sender_id=request.user.id
                    )

            # Broadcast message via WebSockets (graceful fallback if Redis is offline)
            try:
                channel_layer = get_channel_layer()
                if channel_layer:
                    async_to_sync(channel_layer.group_send)(
                        f'chat_{thread.id}',
                        {
                            'type': 'chat_message',
                            'message': msg.text,
                            'file_url': msg.file.url if msg.file else None,
                            'file_name': msg.file.name.split('/')[-1] if msg.file else None,
                            'file_size': msg.file.size if msg.file else None,
                            'sender_id': msg.sender.id,
                            'sender_name': msg.sender.get_full_name() or msg.sender.username,
                            'created_at': msg.created_at.strftime('%H:%M'),
                            'created_at_full': msg.created_at.strftime('%Y-%m-%d %H:%M'),
                            'message_id': msg.id,
                            'is_read': False,
                        }
                    )

                    for user in other_users:
                        async_to_sync(channel_layer.group_send)(
                            f'notifications_{user.id}',
                            {
                                'type': 'send_notification',
                                'notification_id': msg.id,
                                'title': f'Yeni mesaj: {request.user.get_full_name() or request.user.username}',
                                'message': msg.text[:50] + '...' if len(msg.text) > 50 else (msg.text or 'Bir dosya gönderdi'),
                                'thread_id': thread.id,
                                'sender_id': request.user.id,
                                'created_at': msg.created_at.strftime('%H:%M')
                            }
                        )
            except Exception:
                pass

            return JsonResponse({
                'success': True,
                'temp_id': temp_id,
                'message': {
                    'id': msg.id,
                    'text': msg.text,
                    'file_url': msg.file.url if msg.file else None,
                    'file_name': msg.file.name.split('/')[-1] if msg.file else None,
                    'file_size': msg.file.size if msg.file else None,
                    'created_at': msg.created_at.strftime('%H:%M'),
                    'created_at_full': msg.created_at.strftime('%Y-%m-%d %H:%M'),
                    'is_read': msg.is_read,
                    'is_sent': True,
                }
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def start_thread(request):
    """Start a new thread with a selected user."""
    # Sadece staff ve professor rollerine izin ver
    if not hasattr(request.user, 'profile') or request.user.profile.role not in ['staff', 'professor']:
        messages.error(request, 'Bu işlemi yapma yetkiniz yok.')
        return redirect('core:home')

    if request.method == 'POST':
        target_user_id = request.POST.get('target_user_id')
        target_user = get_object_or_404(User, id=target_user_id)
        
        # Hedef kullanıcının da staff veya professor olduğunu kontrol et
        if not hasattr(target_user, 'profile') or target_user.profile.role not in ['staff', 'professor']:
            messages.error(request, 'Bu kullanıcı ile sohbet başlatamazsınız.')
            return redirect('chat:index')

        # Check if thread already exists between these two users (including inactive)
        thread = Thread.objects.filter(
            participants=request.user
        ).filter(
            participants=target_user
        ).first()
        
        if thread:
            # Reactivate the thread if it was previously deleted
            if not thread.is_active:
                thread.is_active = True
                thread.save()
        else:
            # Create a new thread
            thread = Thread.objects.create()
            thread.participants.add(request.user, target_user)
        
        return redirect('chat:index')
    return redirect('chat:index')


@login_required
def mark_as_read(request):
    """Mark messages as read."""
    # Sadece staff ve professor rollerine izin ver
    if not hasattr(request.user, 'profile') or request.user.profile.role not in ['staff', 'professor']:
        return JsonResponse({'error': 'Yetkisiz erişim'}, status=403)

    if request.method == 'POST':
        data = json.loads(request.body)
        thread_id = data.get('thread_id')
        
        try:
            thread = request.user.threads.get(id=thread_id)
            thread.messages.exclude(sender=request.user).filter(is_read=False).update(is_read=True)
            return JsonResponse({'success': True})
        except Thread.DoesNotExist:
            return JsonResponse({'error': 'Thread not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def delete_thread(request, thread_id):
    """Soft delete a thread."""
    # Sadece staff ve professor rollerine izin ver
    if not hasattr(request.user, 'profile') or request.user.profile.role not in ['staff', 'professor']:
        return JsonResponse({'error': 'Yetkisiz erişim'}, status=403)

    if request.method == 'POST':
        try:
            thread = request.user.threads.get(id=thread_id)
            thread.is_active = False
            thread.save()
            return JsonResponse({'success': True})
        except Thread.DoesNotExist:
            return JsonResponse({'error': 'Thread not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def search_users(request):
    """Search for users to start a chat with."""
    # Sadece staff ve professor rollerine izin ver
    if not hasattr(request.user, 'profile') or request.user.profile.role not in ['staff', 'professor']:
        return JsonResponse({'users': []})

    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'users': []})
    
    # Sadece staff ve professor rollerindeki kullanıcıları ara
    users = User.objects.exclude(id=request.user.id).filter(
        Q(username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query)
    ).filter(
        profile__role__in=['staff', 'professor']
    ).select_related('profile')[:10]
    
    data = [{
        'id': user.id,
        'name': user.get_full_name() or user.username,
        'email': user.email,
        'avatar': user.profile.avatar.url if hasattr(user, 'profile') and user.profile.avatar else None,
        'role': user.profile.get_role_display() if hasattr(user, 'profile') else 'User',
    } for user in users]
    
    return JsonResponse({'users': data})


@login_required
def edit_profile(request):
    """ÙˆÛŒØ±Ø§ÛŒØ´ Ù¾Ø±ÙˆÙØ§ÛŒÙ„ Ú©Ø§Ø±Ø¨Ø±"""
    if request.method == 'POST':
        # Ø¨Ø±ÙˆØ²Ø±Ø³Ø§Ù†ÛŒ Ø§Ø·Ù„Ø§Ø¹Ø§Øª Ú©Ø§Ø±Ø¨Ø±
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        
        # Ø¨Ø±ÙˆØ²Ø±Ø³Ø§Ù†ÛŒ Ø¹Ú©Ø³ Ù¾Ø±ÙˆÙØ§ÛŒÙ„
        if request.FILES.get('avatar'):
            # Ø­Ø°Ù Ø¹Ú©Ø³ Ù‚Ø¨Ù„ÛŒ Ø§Ú¯Ø± ÙˆØ¬ÙˆØ¯ Ø¯Ø§Ø±Ø¯
            if hasattr(user, 'profile') and user.profile.avatar:
                if os.path.isfile(user.profile.avatar.path):
                    os.remove(user.profile.avatar.path)
            
            if hasattr(user, 'profile'):
                user.profile.avatar = request.FILES['avatar']
                user.profile.save()
        
        user.save()
        messages.success(request, 'Ù¾Ø±ÙˆÙØ§ÛŒÙ„ Ø¨Ø§ Ù…ÙˆÙÙ‚ÛŒØª Ø¨Ø±ÙˆØ²Ø±Ø³Ø§Ù†ÛŒ Ø´Ø¯.')
        return redirect('chat:index')
    
    # Ø§Ú¯Ø± Ø¯Ø±Ø®ÙˆØ§Ø³Øª GET Ø¨Ø§Ø´Ø¯ØŒ ØµÙØ­Ù‡ ÙˆÛŒØ±Ø§ÛŒØ´ Ù¾Ø±ÙˆÙØ§ÛŒÙ„ Ø±Ø§ Ù†Ù…Ø§ÛŒØ´ Ù…ÛŒâ€ŒØ¯Ù‡ÛŒÙ…
    return render(request, 'chat/edit_profile.html', {'user': request.user})


@login_required

@login_required
def get_notifications(request):
    # Sadece staff ve professor rollerine izin ver
    if not hasattr(request.user, 'profile') or request.user.profile.role not in ['staff', 'professor']:
        return JsonResponse({'error': 'Yetkisiz erişim'}, status=403)

    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:50]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    data = []
    for n in notifications:
        data.append({
            'id': n.id,
            'type': n.notification_type,
            'title': n.title,
            'message': n.message,
            'thread_id': n.thread_id,
            'sender_id': n.sender_id,
            'link_url': n.link_url,
            'is_read': n.is_read,
            'created_at': n.created_at.strftime('%Y-%m-%d %H:%M')
        })
    return JsonResponse({'notifications': data, 'unread_count': unread_count})

@login_required
def mark_notification_read(request):
    # Sadece staff ve professor rollerine izin ver
    if not hasattr(request.user, 'profile') or request.user.profile.role not in ['staff', 'professor']:
        return JsonResponse({'error': 'Yetkisiz erişim'}, status=403)

    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            notification_id = data.get('notification_id')
            if notification_id:
                Notification.objects.filter(id=notification_id, user=request.user).update(is_read=True)
            else:
                Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def _serialize_support_message(msg):
    return {
        'id': msg.id,
        'text': msg.text,
        'sender_name': msg.sender_name,
        'is_staff': msg.is_staff,
        'is_ai': getattr(msg, 'is_ai', False),
        'links': msg.get_links() if hasattr(msg, 'get_links') else (getattr(msg, 'links', None) or []),
        'created_at': msg.created_at.strftime('%H:%M'),
    }


def _broadcast_support_message(session_key, msg):
    try:
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                f'support_{session_key}',
                {
                    'type': 'chat_message',
                    'id': msg.id,
                    'message': msg.text,
                    'sender_name': msg.sender_name,
                    'is_staff': msg.is_staff,
                    'is_ai': msg.is_ai,
                    'links': msg.get_links() if hasattr(msg, 'get_links') else (msg.links or []),
                    'created_at': msg.created_at.strftime('%H:%M'),
                },
            )
    except Exception:
        pass


def _is_valid_support_key(session_key):
    return bool(session_key and len(session_key) >= 8 and re.fullmatch(r'\w+', session_key))


@login_required
def get_support_messages(request, session_key):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Yetkisiz erişim'}, status=403)
    try:
        thread = SupportThread.objects.get(session_key=session_key)
        msgs_qs = thread.support_messages.all().order_by('created_at', 'id')
        after_id = request.GET.get('after_id')
        if after_id and str(after_id).isdigit():
            msgs_qs = msgs_qs.filter(id__gt=int(after_id))
        data = [_serialize_support_message(msg) for msg in msgs_qs]
        return JsonResponse({'success': True, 'messages': data, 'visitor_name': thread.full_name})
    except SupportThread.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Oturum bulunamadı'}, status=404)


def support_init_session(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        payload = {}

    requested_key = (payload.get('session_key') or '').strip()
    full_name = (payload.get('full_name') or 'Ziyaretçi').strip()[:120] or 'Ziyaretçi'
    language = (payload.get('language') or 'tr').strip()[:10] or 'tr'

    owned_keys = list(request.session.get('support_session_keys', []))
    if _is_valid_support_key(requested_key):
        if requested_key in owned_keys or not SupportThread.objects.filter(session_key=requested_key).exists():
            session_key = requested_key
        else:
            session_key = f"vis_{secrets.token_hex(16)}"
    else:
        session_key = f"vis_{secrets.token_hex(16)}"

    thread, created = SupportThread.objects.get_or_create(
        session_key=session_key,
        defaults={'full_name': full_name, 'language': language},
    )
    if not created and full_name and full_name != 'Ziyaretçi' and not thread.full_name:
        thread.full_name = full_name
        thread.language = language
        thread.save(update_fields=['full_name', 'language', 'updated_at'])

    if session_key not in owned_keys:
        owned_keys.append(session_key)
        request.session['support_session_keys'] = owned_keys

    return JsonResponse({
        'success': True,
        'session_key': session_key,
        'visitor_name': thread.full_name,
        'human_handoff': thread.human_handoff,
    })


def support_send_message(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        payload = {}

    session_key = (payload.get('session_key') or '').strip()
    text = (payload.get('message') or '').strip()[:2000]
    visitor_name = (payload.get('sender_name') or 'Ziyaretçi').strip()[:80] or 'Ziyaretçi'

    if not text:
        return JsonResponse({'success': False, 'error': 'Mesaj boş olamaz.'}, status=400)
    if not _is_valid_support_key(session_key):
        return JsonResponse({'success': False, 'error': 'Geçersiz oturum anahtarı.'}, status=400)

    is_staff = bool(request.user.is_authenticated and request.user.is_staff)
    owned_keys = list(request.session.get('support_session_keys', []))

    if not is_staff:
        if session_key not in owned_keys:
            if not SupportThread.objects.filter(session_key=session_key).exists():
                owned_keys.append(session_key)
                request.session['support_session_keys'] = owned_keys
            else:
                return JsonResponse({'success': False, 'error': 'Oturum doğrulanamadı.'}, status=403)
        sender_name = visitor_name
    else:
        sender_name = request.user.get_full_name() or request.user.username

    thread, _ = SupportThread.objects.get_or_create(
        session_key=session_key,
        defaults={'full_name': visitor_name if not is_staff else 'Ziyaretçi'},
    )
    msg = SupportMessage.objects.create(
        thread=thread,
        sender_user=request.user if is_staff else None,
        sender_name=sender_name,
        text=text,
        is_staff=is_staff,
        is_ai=False,
    )
    if is_staff and not thread.human_handoff:
        thread.human_handoff = True
    thread.is_active = True
    thread.save(update_fields=['is_active', 'human_handoff', 'updated_at'])

    _broadcast_support_message(session_key, msg)
    if not is_staff:
        try:
            channel_layer = get_channel_layer()
            if channel_layer:
                async_to_sync(channel_layer.group_send)(
                    'support_staff_notifications',
                    {
                        'type': 'staff_notification',
                        'session_key': session_key,
                        'visitor_name': sender_name,
                        'message': text[:50],
                    },
                )
        except Exception:
            pass

    ai_msg = None
    if not is_staff:
        from .ai_assistant import maybe_reply_as_ai
        ai_msg = maybe_reply_as_ai(thread, text, visitor_name=sender_name)
        if ai_msg:
            _broadcast_support_message(session_key, ai_msg)

    return JsonResponse({
        'success': True,
        'message': _serialize_support_message(msg),
        'ai_message': _serialize_support_message(ai_msg) if ai_msg else None,
        'human_handoff': thread.human_handoff,
    })


def support_set_mode(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        payload = {}

    session_key = (payload.get('session_key') or '').strip()
    mode = (payload.get('mode') or '').strip().lower()
    if mode not in {'ai', 'human'}:
        return JsonResponse({'success': False, 'error': 'Geçersiz mod.'}, status=400)
    if not _is_valid_support_key(session_key):
        return JsonResponse({'success': False, 'error': 'Geçersiz oturum.'}, status=400)

    is_staff = bool(request.user.is_authenticated and request.user.is_staff)
    owned_keys = request.session.get('support_session_keys', [])
    if not is_staff and session_key not in owned_keys:
        return JsonResponse({'success': False, 'error': 'Yetkisiz erişim.'}, status=403)

    thread, _ = SupportThread.objects.get_or_create(
        session_key=session_key,
        defaults={'full_name': 'Ziyaretçi'},
    )
    thread.human_handoff = (mode == 'human')
    thread.is_active = True
    thread.save(update_fields=['human_handoff', 'is_active', 'updated_at'])

    status_msg = None
    if mode == 'human':
        status_msg = SupportMessage.objects.create(
            thread=thread,
            sender_user=None,
            sender_name='Avrasya AI Asistan',
            text='Canlı destek ekibimize bağlantı isteğiniz iletildi. Görevli personelimiz bu pencereden size yanıt verecektir.',
            is_staff=True,
            is_ai=True,
            links=[{'title': 'Yeni Destek Talebi Aç', 'url': '/support/ticket/create/', 'category': 'Destek'}],
        )
        _broadcast_support_message(session_key, status_msg)
        try:
            channel_layer = get_channel_layer()
            if channel_layer:
                async_to_sync(channel_layer.group_send)(
                    'support_staff_notifications',
                    {
                        'type': 'staff_notification',
                        'session_key': session_key,
                        'visitor_name': thread.full_name or 'Ziyaretçi',
                        'message': 'Canlı destek yetkilisi talep edildi',
                    },
                )
        except Exception:
            pass
    else:
        status_msg = SupportMessage.objects.create(
            thread=thread,
            sender_user=None,
            sender_name='Avrasya AI Asistan',
            text='Akıllı Asistan tekrar aktif! Üniversiteyle ilgili her türlü sorunuzu sorabilirsiniz.',
            is_staff=True,
            is_ai=True,
            links=[],
        )
        _broadcast_support_message(session_key, status_msg)

    return JsonResponse({
        'success': True,
        'human_handoff': thread.human_handoff,
        'message': _serialize_support_message(status_msg) if status_msg else None,
    })


def support_poll_messages(request, session_key):
    if not _is_valid_support_key(session_key):
        return JsonResponse({'success': False, 'error': 'Geçersiz oturum'}, status=400)

    is_staff = bool(request.user.is_authenticated and request.user.is_staff)
    owned_keys = request.session.get('support_session_keys', [])
    if not is_staff and session_key not in owned_keys:
        return JsonResponse({'success': False, 'error': 'Yetkisiz erişim'}, status=403)

    thread = SupportThread.objects.filter(session_key=session_key).first()
    if not thread:
        return JsonResponse({'success': True, 'messages': [], 'human_handoff': False})

    msgs_qs = thread.support_messages.all().order_by('created_at', 'id')
    after_id = request.GET.get('after_id')
    if after_id and str(after_id).isdigit():
        msgs_qs = msgs_qs.filter(id__gt=int(after_id))

    return JsonResponse({
        'success': True,
        'messages': [_serialize_support_message(m) for m in msgs_qs],
        'human_handoff': thread.human_handoff,
    })


def voice_assistant_directory(request):
    """Tüm Avrasya Üniversitesi konu ve uygulama dizinini JSON olarak döndürür."""
    from .voice_directory import get_voice_directory
    try:
        directory = get_voice_directory()
        return JsonResponse({'success': True, 'total': len(directory), 'topics': directory}, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def voice_assistant_search(request):
    """Sesli veya yazılı arama sorgusuna göre eşleşen konuları ve canlı içerikleri döndürür."""
    from .voice_directory import search_voice_topics
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'success': True, 'count': 0, 'results': []})

    try:
        results = search_voice_topics(query, max_results=8)
        return JsonResponse({
            'success': True,
            'query': query,
            'count': len(results),
            'results': results
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

