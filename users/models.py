from django.db import models
from django.contrib.auth.models import AbstractUser

# Overriding abstruct user to keep the scope open for future user modification
class CustomUser(AbstractUser):
    pass