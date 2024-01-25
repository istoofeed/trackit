from django import template
from django.contrib.auth.models import Group

from adviser.models import Advisory, PendingAdvisory
from home.models import Notification

register = template.Library()


@register.filter
def in_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False
    return group in user.groups.all()


@register.simple_tag
def get_pending_advisory_count(user):
    return PendingAdvisory.objects.filter(adviser=user).count()


@register.simple_tag
def get_notification_count(user):
    return Notification.objects.filter(receiver=user, is_read=False).count()


@register.simple_tag
def user_in_advisory_group(user):
    user_group = user.group_set.first()
    return Advisory.objects.filter(group=user_group).exists()


@register.filter(name="has_max_advisories")
def has_max_advisories(adviser):
    advisories_count = Advisory.objects.filter(adviser=adviser).count()
    return advisories_count >= 3
