from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q, Count, OuterRef, Subquery
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Thread, Message
import json
from django.contrib import messages
import os

@login_required
def chat_index(request):
    """Render the main chat interface."""
    # Sadece geçerli diğer kullanıcısı olan thread'leri al
    threads = request.user.threads.filter(is_active=True).prefetch_related(
        'participants', 'messages'
    ).annotate(
        unread_count=Count('messages', filter=Q(messages__is_read=False) & ~Q(messages__sender=request.user))
    )
    
    # Get all users for starting new chats (kullanıcıyı hariç tut)
    users = User.objects.exclude(id=request.user.id).select_related('profile')
    
    # Prepare threads data with other participant - sadece geçerli olanları ekle
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
    
    # Eğer hiç geçerli thread yoksa, boş liste gönder
    context = {
        'threads_with_participants': threads_with_participants,
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
    
    # ابتدا کل کوئری را می‌گیریم
    messages_query = thread.messages.select_related('sender').order_by('-created_at')
    
    # ابتدا پیام‌های خوانده نشده را آپدیت می‌کنیم (قبل از اسلایس)
    unread_messages = messages_query.filter(is_read=False).exclude(sender=request.user)
    unread_messages.update(is_read=True, is_delivered=True)
    
    # سپس اسلایس را اعمال می‌کنیم
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
    """AJAX endpoint to send a message to a thread."""
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
        initial_message = request.POST.get('initial_message', '').strip()
        target_user = get_object_or_404(User, id=target_user_id)
        
        # Check if thread already exists between these two users
        thread = Thread.objects.filter(
            participants=request.user
        ).filter(
            participants=target_user
        ).first()
        
        if not thread:
            thread = Thread.objects.create()
            thread.participants.add(request.user, target_user)
            
            # Send initial message if provided
            if initial_message:
                Message.objects.create(
                    thread=thread,
                    sender=request.user,
                    text=initial_message
                )
        
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
    """ویرایش پروفایل کاربر"""
    if request.method == 'POST':
        # بروزرسانی اطلاعات کاربر
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
        
        # بروزرسانی عکس پروفایل
        if request.FILES.get('avatar'):
            # حذف عکس قبلی اگر وجود دارد
            if hasattr(user, 'profile') and user.profile.avatar:
                if os.path.isfile(user.profile.avatar.path):
                    os.remove(user.profile.avatar.path)
            
            if hasattr(user, 'profile'):
                user.profile.avatar = request.FILES['avatar']
                user.profile.save()
        
        user.save()
        messages.success(request, 'پروفایل با موفقیت بروزرسانی شد.')
        return redirect('chat:index')
    
    # اگر درخواست GET باشد، صفحه ویرایش پروفایل را نمایش می‌دهیم
    return render(request, 'chat/edit_profile.html', {'user': request.user})