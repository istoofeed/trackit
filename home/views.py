from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group as UserGroup
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from administrator.filters import TitleFilter
from administrator.models import CapstoneApprovedTitle, Guide
from adviser.models import (
    Advisory,
    Announcement,
    GroupChat,
    GroupChatMessage,
    PendingAdvisory,
    PendingAdvisoryMessage,
    UserTask,
    UserTaskComment,
)
from helpers.decorators import students_only
from users.models import Group, User

from .forms import FileUploadForm, GroupForm, PendingAdvisoryForm, StudentProfileForm
from .models import Notification


@login_required(login_url="users:login_page")
@students_only
def home_page(request):
    tasks = UserTask.objects.filter(student=request.user)
    announcements = Announcement.objects.all()

    context = {"navbar": "home", "tasks": tasks, "announcements": announcements}
    return render(request, "home/home_page.html", context)


@login_required(login_url="users:login_page")
@students_only
def tasks_page(request):
    tasks = UserTask.objects.filter(student=request.user)

    system_tasks = tasks.filter(task__task_type="System")
    document_tasks = tasks.filter(task__task_type="Document")

    context = {
        "navbar": "tasks",
        "tasks": tasks,
        "document_tasks": document_tasks,
        "system_tasks": system_tasks,
    }
    return render(request, "home/tasks_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@students_only
def task_page(request, pk):
    task = get_object_or_404(UserTask, pk=pk, student=request.user)
    comments = UserTaskComment.objects.filter(usertask=task)

    if request.method == "POST":
        comment = request.POST.get("comment")

        if not comment:
            pass
        else:
            UserTaskComment.objects.create(
                usertask=task, user=request.user, comment=comment
            )
        return redirect("student:task_page", task.id)

    context = {"navbar": "tasks", "task": task, "comments": comments}
    return render(request, "home/task_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@students_only
def upload_file(request, pk):
    task = get_object_or_404(UserTask, pk=pk)
    post_url = reverse("student:upload_file", args=[task.id])
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.submitted_by = request.user
            task.submitted_at = timezone.now()
            task.status = "Submitted"
            task.save()

            content = f"{request.user} already submitted their output on task {task.task.title}."

            Notification.objects.create(
                context=content, receiver=task.task.adviser.first()
            )

            return redirect("student:read_file", task.id)

    else:
        form = FileUploadForm(instance=task)

    context = {"navbar": "tasks", "task": task, "form": form, "post_url": post_url}

    return render(request, "components/taskfile_upload_form.html", context)


@login_required(login_url="users:login_page")
@students_only
def read_taskfile(request, pk):
    task = get_object_or_404(UserTask, pk=pk)

    context = {"navbar": "tasks", "task": task}
    return render(request, "components/read_taskfile.html", context)


@login_required(login_url="users:login_page")
@students_only
def capstone_progress_page(request):
    user = request.user
    try:
        group = Group.objects.get(members=user)
    except:
        group = ModuleNotFoundError

    chapters = group.chapters.all()

    context = {"navbar": "capstone_progress", "chapters": chapters, "group": group}
    return render(request, "home/capstone_progress_page.html", context)


@login_required(login_url="users:login_page")
@students_only
def capstone_tracker_page(request, pk):
    group = get_object_or_404(Group, pk=pk)

    chapters = group.chapters.all()

    total_sections = 0
    total_done_sections = 0
    for chapter in chapters:
        total_sections += chapter.total_section
        total_done_sections += chapter.sections.filter(is_done=True).count()

    if total_sections != 0:  # To avoid division by zero
        percentage_done = (total_done_sections / total_sections) * 100
    else:
        percentage_done = 0

    context = {
        "navbar": "capstone_progress",
        "chapters": chapters,
        "group": group,
        "percentage_done": percentage_done,
    }
    return render(request, "home/capstone_tracker_page.html", context)


@login_required(login_url="users:login_page")
@students_only
def guides_page(request):
    guides = Guide.objects.all()

    context = {"navbar": "capstone_progress", "guides": guides}
    return render(request, "home/guides_page.html", context)


@login_required(login_url="users:login_page")
@students_only
def advisers_page(request):
    adviser_group = UserGroup.objects.get(name="adviser")
    advisers = User.objects.filter(groups=adviser_group)
    try:
        group = Group.objects.get(members=request.user)
    except:
        group = None

    if group and Advisory.objects.filter(group=group).exists():
        return redirect("student:home_page")

    pending_requests = PendingAdvisory.objects.filter(group=group)
    adviser_requests = set(
        pending_request.adviser for pending_request in pending_requests
    )

    context = {
        "navbar": "advisers",
        "advisers": advisers,
        "group": group,
        "adviser_requests": adviser_requests,
    }
    return render(request, "home/advisers_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@students_only
def adviser_page(request, pk):
    adviser = User.objects.get(id=pk)
    try:
        group = Group.objects.get(members=request.user)
    except:
        group = None

    if request.method == "POST":
        form = PendingAdvisoryForm(request.POST, request.FILES)
        message = request.POST.get("message")

        if form.is_valid():
            advisory = form.save(commit=False)
            advisory.adviser = adviser
            advisory.group = group
            advisory.save()

            content = (
                f"{group.name} is requesting for your advisory with their research."
            )

            Notification.objects.create(context=content, receiver=adviser)

            if message:
                PendingAdvisoryMessage.objects.create(
                    pending_advisory=advisory, user=request.user, message=message
                )
            return redirect("student:advisers_page")

    else:
        form = PendingAdvisoryForm()

    context = {"navbar": "advisers", "adviser": adviser, "form": form}
    return render(request, "home/adviser_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@students_only
def pending_request_page(request, pk):
    adviser = get_object_or_404(User, pk=pk)
    try:
        group = Group.objects.get(members=request.user)
    except:
        group = None

    if group and Advisory.objects.filter(group=group).exists():
        return redirect("student:home_page")

    pending_advisory = PendingAdvisory.objects.get(adviser=adviser, group=group)

    if request.method == "POST":
        message = request.POST.get("message")

        if message:
            PendingAdvisoryMessage.objects.create(
                pending_advisory=pending_advisory, user=request.user, message=message
            )
            return redirect(request.path)

    context = {
        "navbar": "advisers",
        "pending_advisory": pending_advisory,
    }
    return render(request, "home/pending_request_page.html", context)


@login_required(login_url="users:login_page")
@students_only
def read_comment_logs(request, pk):
    pending_advisory = get_object_or_404(PendingAdvisory, pk=pk)

    return render(
        request,
        "home/htmx/read_comment_logs.html",
        {"pending_advisory": pending_advisory},
    )


@login_required(login_url="users:login_page")
@students_only
def read_pending_advisory(request, pk):
    pending_advisory = get_object_or_404(PendingAdvisory, pk=pk)

    context = {"pending_advisory": pending_advisory}
    return render(request, "home/htmx/read_pending_advisory.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@students_only
def update_pending_advisory(request, pk):
    pending_advisory = get_object_or_404(PendingAdvisory, pk=pk)
    previous_url = reverse("student:read_pending_advisory", args=[pending_advisory.id])

    if request.method == "POST":
        form = PendingAdvisoryForm(
            request.POST, request.FILES, instance=pending_advisory
        )

        if form.is_valid():
            form.save()
            return redirect("student:read_pending_advisory", pending_advisory.id)

    else:
        form = PendingAdvisoryForm(instance=pending_advisory)

    context = {
        "form": form,
        "previous_url": previous_url,
        "pending_advisory": pending_advisory,
    }

    return render(request, "home/htmx/update_pending_advisory.html", context)


@login_required(login_url="users:login_page")
@students_only
def capstone_titles_page(request):
    approved_titles = TitleFilter(
        request.GET, queryset=CapstoneApprovedTitle.objects.all()
    )

    context = {
        "navbar": "capstone_titles",
        "approved_titles": approved_titles.qs,
        "form": approved_titles.form,
    }
    return render(request, "home/capstone_titles_page.html", context)


@login_required(login_url="users:login_page")
@students_only
def capstone_group_page(request):
    user = request.user
    try:
        group = Group.objects.get(members=user)
    except:
        group = ModuleNotFoundError

    context = {"navbar": "capstone_group", "group": group}

    return render(request, "home/capstone_group_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@students_only
def edit_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)

        if form.is_valid():
            form.save()
            return redirect("student:capstone_group_page")
    else:
        form = GroupForm(instance=group)

    context = {"navbar": "capstone_group", "group": group, "form": form}
    return render(request, "home/fn_group.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@students_only
def groupchat_page(request):
    user = request.user
    try:
        group = Group.objects.get(members=user)
    except:
        group = None

    advisory = Advisory.objects.get(group=group)

    groupchat = GroupChat.objects.get(advisory=advisory)

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            GroupChatMessage.objects.create(
                group_chat=groupchat, sender=user, content=content
            )

            return redirect(request.path)

    context = {"navbar": "groupchat", "groupchat": groupchat, "advisory": advisory}
    return render(request, "home/groupchat_page.html", context)


@login_required(login_url="users:login_page")
@students_only
def read_groupchat_logs(request, pk):
    groupchat = get_object_or_404(GroupChat, pk=pk)

    return render(
        request, "home/htmx/read_groupchat_logs.html", {"groupchat": groupchat}
    )


@login_required(login_url="users:login_page")
@students_only
def profile_page(request):
    context = {"navbar": "profile"}
    return render(request, "home/profile_page.html", context)


@login_required(login_url="users:login_page")
@students_only
def notification_page(request):
    notifications = Notification.objects.filter(receiver=request.user)
    for notif in notifications:
        notif.is_read = True
        notif.save()
    context = {"navbar": "notification", "notifications": notifications}
    return render(request, "home/notification_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@students_only
def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.delete()
    return redirect("student:notification_page")


@login_required(login_url="users:login_page")
@students_only
def read_profile_page(request):
    context = {"navbar": "profile"}
    return render(request, "home/read_profile_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@students_only
def update_profile_page(request):
    user = request.user
    previous_url = reverse("student:profile_page")
    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect("student:read_profile_page")
    else:
        form = StudentProfileForm(instance=user)

    context = {"navbar": "profile", "form": form, "previous_url": previous_url}

    return render(request, "home/update_profile_page.html", context)
