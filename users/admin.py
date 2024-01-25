from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Chapter, Group, Section, User

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Chapter)
admin.site.register(Section)
