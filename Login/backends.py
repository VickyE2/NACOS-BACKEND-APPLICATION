from django.contrib.auth.backends import ModelBackend, UserModel

class UsernameAuthentication(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check if the person exists by username
        try:
            user = UserModel.objects.get(
                username=username
            )
        except UserModel.DoesNotExist:
            return None

        # Check if the password is correct
        if user.check_password(password):
            return user
        return None