from core.models import Notification

def notifications_processor(request):
    """
    Контекстный процессор, добавляющий уведомления пользователя в контекст шаблона.
    """
    context = {}
    
    if request.user.is_authenticated and not request.user.is_superuser:
        # Все уведомления пользователя (как прочитанные, так и непрочитанные)
        all_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        
        # Только непрочитанные уведомления для счетчика
        unread_notifications = all_notifications.filter(is_read=False)
        
        context['notifications'] = all_notifications
        context['unread_notifications_count'] = unread_notifications.count()
    else:
        context['notifications'] = []
        context['unread_notifications_count'] = 0
        
    return context 