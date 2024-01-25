from django.contrib import admin

from .models import (
    Advisory,
    Announcement,
    GroupChat,
    PendingAdvisory,
    PendingAdvisoryMessage,
    Task,
    UserTask,
    UserTaskComment,
)

admin.site.register(Task)
admin.site.register(UserTask)
admin.site.register(UserTaskComment)
admin.site.register(Announcement)
admin.site.register(Advisory)
admin.site.register(PendingAdvisory)
admin.site.register(PendingAdvisoryMessage)
admin.site.register(GroupChat)
