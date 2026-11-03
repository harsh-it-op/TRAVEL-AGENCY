"""Context processor to inject logged-in Tourly user from Django session into all templates."""
from .models import User


def tourly_session_user(request):
    user_id = request.session.get('tourly_user_id')
    current_user = None
    if user_id:
        try:
            current_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            request.session.flush()
    return {
        'tourly_user': current_user,
        'is_admin_session': bool(request.session.get('tourly_is_admin', False)),
    }
