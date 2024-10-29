from django.contrib.auth.models import AbstractUser

# This is like the....... user....uhm the way you get or put a user is defined by this...

class BaseUser(AbstractUser):
    def __str__(self):
        return self.get_username
