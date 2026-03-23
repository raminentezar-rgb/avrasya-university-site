from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.utils import timezone
from .models import Thread, Message, Notification
import json
from django.contrib import messages
import os
from django.utils.timesince import timesince


@login_required
def chat_index(request):
    """Render the main chat interface."""
    # Sadece geÃ§erli diÄŸer kullanÄ±cÄ±sÄ± olan thread'leri al
    threads = request.user.threads.filter(is_active=True).prefetch_related(
        'participants', 'messages'
    ).annotate(
        unread_count=Count('messages', filter=Q(messages__is_read=False) & ~Q(messages__sender=request.user))
    )
    
    # Get all users for starting new chats (kullanÄ±cÄ±yÄ± hariÃ§ tut)
    users = User.objects.exclude(id=request.user.id).select_related('profile')
    
    # Prepare support threads for staff
    support_threads = []
    if request.user.is_staff:
        from .models import SupportThread
        support_threads = SupportThread.objects.filter(is_active=True).order_by('-updated_at')
    
    # Prepare threads data with other participant - sadece geÃ§erli olanlarÄ± ekle
    threads_with_participants = []
    for thread in threads:
        other_user = thread.get_other_participant(request.user)
        if other_user:  # Sadece other_user varsa ekle
            threads_with_participants.append({
                'thread': thread,
                'other_user': other_user,
                'unread_count': getattr(thread, 'unread_count', 0),
                'last_message': thread.get_last_message()
            })
    
    # EÄŸer hiÃ§ geÃ§erli thread yoksa, boÅŸ liste gÃ¶nder
    context = {
        'threads_with_participants': threads_with_participants,
        'support_threads': support_threads,
        'users': users,
        'has_valid_threads': len(threads_with_participants) > 0,
        'first_valid_thread': threads_with_participants[0] if threads_with_participants else None
    }
    return render(request, 'chat/index.html', context)


@login_required
def thread_messages(request, thread_id):
    """Return JSON list of messages for a given thread."""
    try:
        thread = request.user.threads.get(id=thread_id)
    except Thread.DoesNotExist:
        return JsonResponse({'error': 'Thread not found'}, status=404)
    
    # Get messages with pagination
    page = int(request.GET.get('page', 1))
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
    if request.method == 'POST':
        thread_id = request.POST.get('thread_id')
        text = request.POST.get('text', '').strip()
        file = request.FILES.get('file')
        temp_id = request.POST.get('temp_id')

        try:
            thread = request.user.threads.get(id=thread_id)
        except Thread.DoesNotExist:
            return JsonResponse({'error': 'Thread not found'}, status=404)

        if text or file:
            msg = Message.objects.create(
                thread=thread,
                sender=request.user,
                text=text,
                file=file
            )
            
            # Ø§Ø±Ø³Ø§Ù„ Ù†ÙˆØªÛŒÙÛŒÚ©ÛŒØ´Ù† Ø¨Ù‡ Ø³Ø§ÛŒØ± Ø´Ø±Ú©Øªâ€ŒÚ©Ù†Ù†Ø¯Ú¯Ø§Ù†
            other_users = thread.participants.exclude(id=request.user.id)
            for user in other_users:
                if text:  # ÙÙ‚Ø· Ø§Ú¯Ø± Ù…ØªÙ† ÙˆØ¬ÙˆØ¯ Ø¯Ø§Ø´Øª Ù†ÙˆØªÛŒÙÛŒÚ©ÛŒØ´Ù† Ø¨ÙØ±Ø³Øª
                    Notification.objects.create(
                        user=user,
                        notification_type='message',
                        title=f'Yeni mesaj: {request.user.get_full_name() or request.user.username}',
                        message=text[:100] + '...' if len(text) > 100 else text,
                        thread_id=thread.id,
                        sender_id=request.user.id
                    )
                elif file:  # Ø§Ú¯Ø± ÙØ§ÛŒÙ„ Ø¨ÙˆØ¯
                    Notification.objects.create(
                        user=user,
                        notification_type='message',
                        title=f'Yeni dosya: {request.user.get_full_name() or request.user.username}',
                        message='Bir dosya gÃ¶nderdi',
                        thread_id=thread.id,
                        sender_id=request.user.id
                    )

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
    if request.method == 'POST':
        target_user_id = request.POST.get('target_user_id')
        target_user = get_object_or_404(User, id=target_user_id)
        
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
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'users': []})
    
    users = User.objects.exclude(id=request.user.id).filter(
        Q(username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query)
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
            'is_read': n.is_read,
            'created_at': n.created_at.strftime('%Y-%m-%d %H:%M')
        })
    return JsonResponse({'notifications': data, 'unread_count': unread_count})

@login_required
def mark_notification_read(request):
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

@login_required
def get_support_messages(request, session_key):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Yetkisiz erişim'})
    from .models import SupportThread, SupportMessage
    try:
        thread = SupportThread.objects.get(session_key=session_key)
        messages = thread.support_messages.all().order_by('created_at')
        data = []
        for msg in messages:
            data.append({
                'text': msg.text,
                'sender_name': msg.sender_name,
                'is_staff': msg.is_staff,
                'created_at': msg.created_at.strftime('%H:%M')
            })
        return JsonResponse({'success': True, 'messages': data, 'visitor_name': thread.full_name})
    except SupportThread.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Oturum bulunamadı'})
