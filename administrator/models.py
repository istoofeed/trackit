from django.db import models

from users.models import Group, User


class GroupAdvisory(models.Model):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    adviser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class CapstoneApprovedTitle(models.Model):
    capstone_title = models.CharField(max_length=355, blank=True)
    group_members = models.CharField(max_length=255, blank=True)
    capstone_adviser = models.CharField(max_length=255, blank=True)
    file = models.FileField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Guide(models.Model):
    content = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
