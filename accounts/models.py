from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    affiliation = models.CharField(max_length=255, blank=True)
    homepage = models.URLField(blank=True)
    scholar = models.URLField(blank=True)
    github = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} Profile"
