from django.contrib.auth.backends import ModelBackend, UserModel

class EmailModelBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        # Check if the person exists by email
        try:
            user = UserModel.objects.get(
                email=email
            )
        except UserModel.DoesNotExist:
            return None

        # Check if the password is correct
        if user.check_password(password):
            return user
        return None