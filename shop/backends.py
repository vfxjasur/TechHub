from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Normalize phone number (remove spaces, dashes, etc.)
        normalized_phone = username.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        try:
            # Try to find user by phone number
            profile = UserProfile.objects.get(phone=normalized_phone)
            user = profile.user
        except UserProfile.DoesNotExist:
            # If not found by phone, try regular username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Try with normalized phone as username
                try:
                    user = User.objects.get(username=normalized_phone)
                except User.DoesNotExist:
                    return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
