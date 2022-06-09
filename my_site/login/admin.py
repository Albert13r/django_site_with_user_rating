from django.contrib import admin

from .models import SiteUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'personal_invite_code',
                    'invite_code',
                    'points')
    search_fields = ('username', 'id', 'personal_invite_code', 'invite_code', 'points')


admin.site.register(SiteUser, UserAdmin)
