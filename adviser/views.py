from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from administrator.filters import TitleFilter
from administrator.models import CapstoneApprovedTitle, Guide
from helpers.decorators import allowed_user
from home.models import Notification
from users.models import Chapter, Group, Section

from .forms import AdviserProfileForm, AnnouncementForm, RevisionForm, TaskForm
from .models import (
    Advisory,
    Announcement,
    GroupChat,
    GroupChatMessage,
    PendingAdvisory,
    PendingAdvisoryMessage,
    Task,
    UserTask,
    UserTaskComment,
)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def home_page(request):
    user = request.user
    tasks = user.advised_tasks.all()
    announcements = Announcement.objects.filter(adviser=request.user)

    context = {
        "navbar": "home",
        "tasks": tasks,
        "announcements": announcements,
    }

    return render(request, "adviser/home_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def tasks_page(request):
    tasks = Task.objects.filter(adviser=request.user).order_by("created_at")

    context = {"navbar": "tasks", "tasks": tasks}
    return render(request, "adviser/tasks_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def users_tasks_page(request, pk):
    task = get_object_or_404(Task, pk=pk)

    context = {"navbar": "tasks", "task": task}
    return render(request, "adviser/users_tasks_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def usertask_details_page(request, pk):
    usertask = get_object_or_404(UserTask, pk=pk)
    comments = UserTaskComment.objects.filter(usertask=usertask)

    if request.method == "POST":
        comment = request.POST.get("comment")

        if comment:
            UserTaskComment.objects.create(
                usertask=usertask, user=request.user, comment=comment
            )

        return redirect("adviser:usertask_details_page", usertask.id)

    context = {"navbar": "tasks", "usertask": usertask, "comments": comments}
    return render(request, "adviser/usertask_details_page.html", context)


@csrf_exempt
def need_revision(request, pk):
    usertask = get_object_or_404(UserTask, pk=pk)
    task = usertask.task

    if request.method == "POST":
        form = RevisionForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            usertask.status = "For Revision"
            usertask.save()

            comment = request.POST.get("comment")
            if comment:
                UserTaskComment.objects.create(
                    usertask=usertask, user=request.user, comment=comment
                )

            return redirect("adviser:usertask_details_page", usertask.id)
    else:
        form = RevisionForm(instance=task)

    context = {"navbar": "tasks", "usertask": usertask, "form": form}

    return render(request, "adviser/need_revision.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def create_task_page(request):
    adviser = request.user
    adviser_groups = Advisory.objects.filter(adviser=adviser)

    if request.method == "POST":
        form = TaskForm(adviser, request.POST)

        # selected_groups = request.POST.getlist("selected_groups")

        # if not selected_groups:
        #     messages.error(request, "Please select a group")
        #     return redirect(request.path)

        if form.is_valid():
            task = form.save()
            task.adviser.add(adviser)
            task.save()

            groups = request.POST.getlist("groups")
            for group_id in groups:
                group = Group.objects.get(id=group_id)
                for user in group.members.all():
                    UserTask.objects.create(task=task, student=user)
            return redirect("adviser:home_page")
    else:
        form = TaskForm(adviser)

    context = {
        "navbar": "home",
        "form": form,
        "fn": "create",
        "adviser_groups": adviser_groups,
    }
    return render(request, "adviser/fn_task_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def update_task_page(request, pk):
    adviser = request.user
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(adviser, request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("adviser:home_page")
    else:
        form = TaskForm(adviser, instance=task)

    context = {"navbar": "home", "form": form, "fn": "update", "task": task}

    return render(request, "adviser/fn_task_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect("adviser:home_page")


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def create_announcement_page(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.adviser = request.user
            announcement.save()
            return redirect("adviser:home_page")
    else:
        form = AnnouncementForm()

    context = {"navbar": "home", "fn": "create", "form": form}
    return render(request, "adviser/fn_announcement_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def update_announcement_page(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect("adviser:home_page")
    else:
        form = AnnouncementForm(instance=announcement)

    context = {"navbar": "home", "fn": "update", "form": form}
    return render(request, "adviser/fn_announcement_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.delete()
    return redirect("adviser:home_page")


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def advisories_page(request):
    advisories = Advisory.objects.filter(adviser=request.user)

    context = {"navbar": "advisories", "advisories": advisories}
    return render(request, "adviser/advisories_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def groupchat_page(request, pk):
    group = get_object_or_404(Group, pk=pk)
    advisory = Advisory.objects.get(group=group)
    groupchat = GroupChat.objects.get(advisory=advisory)

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            GroupChatMessage.objects.create(
                group_chat=groupchat, sender=request.user, content=content
            )

            return redirect(request.path)

    context = {"navbar": "advisories", "group": group, "groupchat": groupchat}
    return render(request, "adviser/groupchat_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def read_groupchat_logs(request, pk):
    groupchat = get_object_or_404(GroupChat, pk=pk)

    return render(
        request, "adviser/htmx/read_groupchat_logs.html", {"groupchat": groupchat}
    )


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def capstone_progress_tracker_page(request, pk):
    group = get_object_or_404(Group, pk=pk)
    chapters = group.chapters.all()

    for chapter in chapters:
        sections = chapter.sections.all()
        totalSection = sections.count()

        sectionFinished = sections.filter(is_done=True).count()

        progress = (sectionFinished / totalSection) * 100

        chapter.total_section = totalSection
        chapter.chapter_progress = progress
        chapter.is_done = progress == 100
        chapter.save()

    context = {"navbar": "advisories", "group": group, "chapters": chapters}
    return render(request, "adviser/capstone_progress_tracker_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def capstone_progress(request, pk):
    group = get_object_or_404(Group, pk=pk)
    chapters = group.chapters.all()

    total_sections = 0
    total_done_sections = 0
    for chapter in chapters:
        total_sections += chapter.total_section
        total_done_sections += chapter.sections.filter(is_done=True).count()

    percentage_done = (total_done_sections / total_sections) * 100

    context = {
        "navbar": "advisories",
        "group": group,
        "chapters": chapters,
        "percentage_done": percentage_done,
    }
    return render(request, "adviser/capstone_progress.html", context)


def first_section_done(request, pk):
    section = get_object_or_404(Section, pk=pk)
    chapter = section.chapter

    section.date_finished = datetime.now()
    section.is_done = True
    section.save()

    chapter.date_started = datetime.now()
    chapter.save()

    sections = chapter.sections.all()
    sectionFinished = sections.filter(is_done=True).count()
    section_count = sections.count()

    if sectionFinished == section_count:
        chapter.date_ended = datetime.now()
        chapter.save()
    return redirect(request.META.get("HTTP_REFERER"))


def section_done(request, pk):
    section = get_object_or_404(Section, pk=pk)
    chapter = section.chapter

    section.date_finished = datetime.now()
    section.is_done = True
    section.save()

    sections = chapter.sections.all()
    sectionFinished = sections.filter(is_done=True).count()
    section_count = sections.count()

    if sectionFinished == section_count:
        chapter.date_ended = datetime.now()
        chapter.save()
    return redirect(request.META.get("HTTP_REFERER"))


def last_section_done(request, pk):
    section = get_object_or_404(Section, pk=pk)
    chapter = section.chapter

    section.date_finished = datetime.now()
    section.is_done = True
    section.save()

    sections = chapter.sections.all()
    sectionFinished = sections.filter(is_done=True).count()
    section_count = sections.count()

    if sectionFinished == section_count:
        chapter.date_ended = datetime.now()
        chapter.save()
    return redirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def advisory_group_details_page(request):
    context = {"navbar": "advisories"}
    return render(request, "adviser/advisory_group_details_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def capstone_approved_titles_page(request):
    approved_titles = TitleFilter(
        request.GET, queryset=CapstoneApprovedTitle.objects.all()
    )

    context = {
        "navbar": "capstone_approved_titles",
        "approved_titles": approved_titles.qs,
        "form": approved_titles.form,
    }
    return render(request, "adviser/capstone_approved_titles_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def capstone_group_requests_page(request):
    pending_requests = PendingAdvisory.objects.filter(adviser=request.user)

    context = {
        "navbar": "capstone_group_requests",
        "pending_requests": pending_requests,
    }
    return render(request, "adviser/capstone_group_requests_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def request_details_page(request, pk):
    pending_advisory = get_object_or_404(PendingAdvisory, pk=pk)

    if pending_advisory.is_read == False:
        for user in pending_advisory.group.members.all():
            content = f"{request.user.name} is currently reviewing your request. Waiting for his/her response"
            Notification.objects.create(context=content, receiver=user)
        pending_advisory.is_read = True
        pending_advisory.save()

    if request.method == "POST":
        message = request.POST.get("message")

        if message:
            PendingAdvisoryMessage.objects.create(
                pending_advisory=pending_advisory, user=request.user, message=message
            )
            return redirect(request.path)

    context = {
        "navbar": "capstone_group_requests",
        "pending_advisory": pending_advisory,
    }
    return render(request, "adviser/request_details_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def read_comment_logs(request, pk):
    pending_advisory = get_object_or_404(PendingAdvisory, pk=pk)

    return render(
        request,
        "adviser/htmx/read_comment_logs.html",
        {"pending_advisory": pending_advisory},
    )


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def reject_request(request, pk):
    group_request = get_object_or_404(PendingAdvisory, pk=pk)
    group_request.delete()
    for user in group_request.group.members.all():
        content = f"{request.user.name} has rejected your advisory request."
        Notification.objects.create(context=content, receiver=user)
    return redirect("adviser:capstone_group_requests_page")


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def accept_request(request, pk):
    group_request = get_object_or_404(PendingAdvisory, pk=pk)
    group = group_request.group

    Advisory.objects.create(group=group, adviser=request.user)
    PendingAdvisory.objects.filter(group=group).delete()

    for user in group.members.all():
        content = f"{request.user.name} has accepted your advisory request."
        Notification.objects.create(context=content, receiver=user)

    return redirect("adviser:advisories_page")


def notification_page(request):
    notifications = Notification.objects.filter(receiver=request.user)

    for notif in notifications:
        notif.is_read = True
        notif.save()

    context = {"navbar": "notification", "notifications": notifications}

    return render(request, "adviser/notification_page.html", context)


def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.delete()
    return redirect("adviser:notification_page")


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def profile_page(request):
    context = {"navbar": "profile"}
    return render(request, "adviser/profile_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def read_profile_page(request):
    context = {"navbar": "profile"}
    return render(request, "adviser/read_profile_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def update_profile_page(request):
    user = request.user
    previous_url = reverse("adviser:profile_page")
    if request.method == "POST":
        form = AdviserProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect("adviser:read_profile_page")
    else:
        form = AdviserProfileForm(instance=user)

    context = {"navbar": "profile", "form": form, "previous_url": previous_url}

    return render(request, "adviser/update_profile_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["adviser"])
def guides(request):
    guides = Guide.objects.all()
    context = {
        "navbar": "guides",
        "guides": guides,
    }

    return render(request, "adviser/guides.html", context)
