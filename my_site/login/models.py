from django.db import models


class SiteUser(models.Model):
    username = models.CharField(max_length=70, verbose_name='Username', unique=True)
    email = models.EmailField(verbose_name='Email', unique=True)
    date_joined = models.DateTimeField(auto_now=True, verbose_name='Data joined')
    is_active = models.BooleanField(default=False, verbose_name='Activity status')
    is_verified = models.BooleanField(default=False, verbose_name='Verified status')
    is_staff = models.BooleanField(default=False, verbose_name="Staff")
    personal_invite_code = models.CharField(max_length=70, verbose_name='Personal invite code')
    invite_code = models.CharField(max_length=70, verbose_name='Invite code', blank=True)
    points = models.IntegerField(verbose_name='Points', default=0)

    def __str__(self):
        return self.username

