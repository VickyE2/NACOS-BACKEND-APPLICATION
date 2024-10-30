from django.contrib.auth.models import AbstractUser


class BaseUser(AbstractUser):
    def __str__(self):
        return self.username