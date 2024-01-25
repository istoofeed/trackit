from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from helpers.models import TrackingModel
from users.models import Group as UserGroup
from users.models import User


class Task(TrackingModel):
    TASK_TYPE = (
        ("Document", "Document"),
        ("System", "System"),
    )
    # task_no = models.IntegerField(blank=True, unique=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField(blank=True)
    # grades = models.IntegerField(null=True, blank=True)
    adviser = models.ManyToManyField(User, related_name="advised_tasks", blank=True)
    task_type = models.TextField(max_length=255, blank=True, choices=TASK_TYPE)

    def __str__(self):
        return self.title

    # Am I doing this right?
    def get_submitted_user_task_count(self):
        return self.usertask_set.filter(
            status__in=["Submitted", "For Revision"]
        ).count()


# class TaskAssignment(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)


class UserTask(models.Model):
    TASK_STATUS = (
        ("Not Yet Submitted", "Not Yet Submitted"),
        ("Submitted", "Submitted"),
        ("For Revision", "For Revision"),
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(blank=True)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    user_grades = models.IntegerField(null=True, blank=True)
    status = models.CharField(default="Not Yet Submitted", max_length=255)
    submitted_at = models.DateTimeField(auto_now_add=True, editable=True)
    modified_at = models.DateTimeField(auto_now=True)
    revised_count = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.task.title

    class Meta:
        ordering = ["task__created_at", "status"]


class UserTaskComment(models.Model):
    usertask = models.ForeignKey(
        UserTask, on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(blank=True)
    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Announcement(TrackingModel):
    header = models.CharField(max_length=150, blank=True)
    body = models.TextField(blank=True)
    adviser = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.header


class Advisory(models.Model):
    group = models.ForeignKey(
        UserGroup, on_delete=models.CASCADE, null=True, blank=True
    )
    adviser = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.adviser.username


@receiver(post_save, sender=Advisory)
def create_groupchat(sender, instance, created, **kwargs):
    if created:
        GroupChat.objects.create(advisory=instance)


class PendingAdvisory(models.Model):
    group = models.ForeignKey(
        UserGroup, on_delete=models.CASCADE, null=True, blank=True
    )
    proposed_title = models.CharField(max_length=255, blank=True)
    adviser = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(blank=True)
    is_read = models.BooleanField(default=False)

    def get_pending_request_count(cls, user):
        return cls.objects.filter(adviser=user).count()


class PendingAdvisoryMessage(models.Model):
    pending_advisory = models.ForeignKey(
        PendingAdvisory, on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class GroupChat(models.Model):
    advisory = models.ForeignKey(Advisory, on_delete=models.CASCADE)


class GroupChatMessage(models.Model):
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
