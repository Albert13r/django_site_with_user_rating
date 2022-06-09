from django.contrib.auth.models import User
from django.db import models


class SiteUser(User):
    personal_invite_code = models.CharField(max_length=70, verbose_name='Personal invite code')
    invite_code = models.CharField(max_length=70, verbose_name='Invite code', blank=True)
    points = models.IntegerField(verbose_name='Points', default=0)

    def __str__(self):
        return self.username

