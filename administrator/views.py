import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group as BaseGroup
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from adviser.forms import AnnouncementForm
from adviser.models import Advisory, Announcement, Task, UserTask
from helpers.decorators import allowed_user
from users.models import Group, User

from .filters import TitleFilter
from .forms import ApprovedTitleForm, GroupAdvisoryForm, GuideForm, SignupForm, TaskForm
from .models import CapstoneApprovedTitle, GroupAdvisory, Guide


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def home_page(request):
    tasks = Task.objects.filter(adviser=request.user)
    announcements = Announcement.objects.filter(adviser=request.user)

    context = {
        "navbar": "home",
        "tasks": tasks,
        "announcements": announcements,
    }
    return render(request, "administrator/home_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def create_task_page(request):
    adviser = request.user

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save()
            task.adviser.add(adviser)
            task.save()

            groups = request.POST.getlist("groups")
            for group_id in groups:
                group = Group.objects.get(id=group_id)
                advisory = Advisory.objects.get(group=group)
                task.adviser.add(advisory.adviser)
                task.save()
                for user in group.members.all():
                    UserTask.objects.create(task=task, student=user)
            return redirect("administrator:home_page")

    else:
        form = TaskForm()

    context = {
        "navbar": "home",
        "form": form,
        "fn": "create",
    }

    return render(request, "administrator/fn_task_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def update_task_page(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("administrator:home_page")
    else:
        form = TaskForm(instance=task)

    context = {"navbar": "home", "form": form, "fn": "update", "task": task}

    return render(request, "administrator/fn_task_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect("administrator:home_page")


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
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
    return render(request, "administrator/fn_announcement_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
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
    return render(request, "administrator/fn_announcement_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.delete()
    return redirect("administrator:home_page")


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def capstone_progress_tracker_page(request):
    groups = Group.objects.all()
    group_percentages = []
    for group in groups:
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
        group_percentages.append(round(percentage_done, 2))

    context = {
        "navbar": "capstone_progress_tracker",
        "groups": zip(groups, group_percentages),
    }
    return render(request, "administrator/capstone_progress_tracker_page.html", context)


def capstone_progress(request, pk):
    group = get_object_or_404(Group, pk=pk)
    chapters = group.chapters.all()
    context = {
        "navbar": "capstone_progress_tracker",
        "group": group,
        "chapters": chapters,
    }
    return render(request, "administrator/capstone_progress.html", context)


def capstone_tracker(request, pk):
    group = get_object_or_404(Group, pk=pk)
    chapters = group.chapters.all()

    total_sections = 0
    total_done_sections = 0
    for chapter in chapters:
        total_sections += chapter.total_section
        total_done_sections += chapter.sections.filter(is_done=True).count()

    if total_sections != 0:
        percentage_done = (total_done_sections / total_sections) * 100
    else:
        percentage_done = 0

    context = {
        "navbar": "capstone_progress_tracker",
        "chapters": chapters,
        "group": group,
        "percentage_done": percentage_done,
    }
    return render(request, "administrator/capstone_tracker.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def advisories_page(request):
    group_advisories = GroupAdvisory.objects.all()

    context = {"navbar": "advisories", "group_advisories": group_advisories}
    return render(request, "administrator/advisories_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def create_groupadvisory_page(request):
    if request.method == "POST":
        form = GroupAdvisoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("administrator:advisories_page")
    else:
        form = GroupAdvisoryForm()

    context = {"navbar": "advisories", "form": form, "fn": "create"}

    return render(request, "administrator/fn_groupadvisory_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def update_groupadvisory_page(request, pk):
    group_advisory = get_object_or_404(GroupAdvisory, pk=pk)
    if request.method == "POST":
        form = GroupAdvisoryForm(request.POST, instance=group_advisory)
        if form.is_valid():
            form.save()
            return redirect("administrator:advisories_page")
    else:
        form = GroupAdvisoryForm(instance=group_advisory)

    context = {"navbar": "advisories", "form": form, "fn": "update"}

    return render(request, "administrator/fn_groupadvisory_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def delete_groupadvisory(request, pk):
    group_advisory = get_object_or_404(GroupAdvisory, pk=pk)
    group_advisory.delete()
    return redirect("administrator:advisories_page")


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def approved_capstone_titles_page(request):
    approved_titles = TitleFilter(
        request.GET, queryset=CapstoneApprovedTitle.objects.all()
    )

    context = {
        "navbar": "approved_capstone_titles",
        "approved_titles": approved_titles.qs,
        "form": approved_titles.form,
    }
    return render(request, "administrator/approved_capstone_titles_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def create_approved_title_page(request):
    if request.method == "POST":
        form = ApprovedTitleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("administrator:approved_capstone_titles_page")
    else:
        form = ApprovedTitleForm()

    context = {"navbar": "advisories", "form": form, "fn": "create"}

    return render(request, "administrator/fn_approved_title_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def update_approved_title_page(request, pk):
    approved_title = get_object_or_404(CapstoneApprovedTitle, pk=pk)
    if request.method == "POST":
        form = ApprovedTitleForm(request.POST, request.FILES, instance=approved_title)
        if form.is_valid():
            form.save()
            return redirect("administrator:approved_capstone_titles_page")
    else:
        form = ApprovedTitleForm(instance=approved_title)

    context = {"navbar": "advisories", "form": form, "fn": "update"}

    return render(request, "administrator/fn_approved_title_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def delete_approved_title(request, pk):
    approved_title = get_object_or_404(CapstoneApprovedTitle, pk=pk)
    approved_title.delete()
    return redirect("administrator:approved_capstone_titles_page")


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def groupchat_page(request):
    context = {"navbar": "groupchat"}
    return render(request, "administrator/groupchat_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def capstone_group_page(request):
    groups = Group.objects.filter(is_approved=False)
    users_in_group = User.objects.filter(groups__name="student")
    approved_groups = Group.objects.filter(is_approved=True).count()
    context = {
        "navbar": "capstone_group",
        "groups": groups,
        "users_in_group": users_in_group,
        "approved_groups": approved_groups,
    }

    return render(request, "administrator/capstone_group_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def approved_group_page(request):
    groups = Group.objects.filter(is_approved=True)
    context = {
        "navbar": "capstone_group",
        "groups": groups,
    }

    return render(request, "administrator/approved_group_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def advisers_page(request):
    users_in_group = User.objects.filter(groups__name="adviser")
    students = False
    context = {
        "navbar": "profile",
        "not_active": "students",
        "users_in_group": users_in_group,
        "students": students,
    }
    return render(request, "administrator/users_page.html", context)


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def users_page(request):
    users_in_group = User.objects.filter(groups__name="student")
    students = True
    student_count = users_in_group.count()
    context = {
        "navbar": "profile",
        "not_active": "advisers",
        "users_in_group": users_in_group,
        "students": students,
        "student_count": student_count,
    }
    return render(request, "administrator/users_page.html", context)


@csrf_exempt
@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def add_users(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            name = request.POST.get("name")
            course = request.POST.get("course")
            user_type = request.POST.get("user_type")
            user_role = request.POST.get("user_role")
            specialized_in = request.POST.get("specialized_in")
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()
            user.name = name
            user.course = course
            user.user_role = user_role
            user.specialized_in = specialized_in
            user.save()

            if user_type == "student":
                group = BaseGroup.objects.get(name="student")
                user.groups.add(group)
                return redirect("administrator:users_page")
            if user_type == "adviser":
                group = BaseGroup.objects.get(name="adviser")
                user.groups.add(group)
                return redirect("administrator:advisers_page")

    else:
        form = SignupForm()

    context = {
        "form": form,
    }

    return render(request, "administrator/add_users.html", context)


def delete_user(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def create_groupings(request):
    students = User.objects.filter(groups__name="student", in_group=False)

    # ! Remove this when in Production
    groups = Group.objects.all()
    unapproved_groups = groups.filter(is_approved=False)
    unapproved_groups.delete()

    shuffled_students = random.sample(list(students), len(students))
    random.shuffle(shuffled_students)

    group_size = 3
    num_students = len(students)

    approved_group = groups.filter(is_approved=True).count()
    with transaction.atomic():
        for i in range(num_students // group_size):
            group_name = f"Group {i+1+approved_group}"

            try:
                group = Group.objects.create(name=group_name)

                for j in range(group_size):
                    student = shuffled_students[i * group_size + j]
                    group.members.add(student)

            except Exception as e:
                print(f"Error creating group {group_name}: {e}")

        remaining_students = num_students % group_size
        if remaining_students > 0:
            for i in range(remaining_students):
                student = shuffled_students[num_students - remaining_students + i]
                group_name = f"Group {i % (num_students // group_size) + 1}"
                group = Group.objects.get(name=group_name)
                group.members.add(student)

    return redirect("administrator:capstone_group_page")


def approved_group(request, pk):
    groups = Group.objects.filter(is_approved=True).count()
    group = get_object_or_404(Group, pk=pk)
    for user in group.members.all():
        user.in_group = True
        user.save()

        group.name = f"Group {groups+1}"
        group.is_approved = True
        group.save()
    return redirect("administrator:capstone_group_page")


def delete_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    for user in group.members.all():
        user.in_group = False
        user.save()

        group.is_approved = False
        group.save()
    return redirect("administrator:capstone_group_page")


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def delete_all_groups(request):
    groups = Group.objects.all()
    groups.delete()
    return redirect("administrator:capstone_group_page")


@login_required(login_url="users:login_page")
@allowed_user(allowed_roles=["admin"])
def guides(request):
    guides = Guide.objects.all()
    context = {
        "navbar": "guides",
        "guides": guides,
    }

    return render(request, "administrator/guides.html", context)


@csrf_exempt
def add_guide(request):
    if request.method == "POST":
        form = GuideForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("administrator:guides")
    else:
        form = GuideForm()

    context = {"navbar": "guides", "form": form, "fn": "create"}

    return render(request, "administrator/fn_guide.html", context)


@csrf_exempt
def edit_guide(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    if request.method == "POST":
        form = GuideForm(request.POST, instance=guide)
        if form.is_valid():
            form.save()
            return redirect("administrator:guides")
    else:
        form = GuideForm(instance=guide)

    context = {"navbar": "guides", "form": form, "fn": "update"}

    return render(request, "administrator/fn_guide.html", context)


def delete_guide(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    guide.delete()
    return redirect("administrator:guides")
