from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from helpers.decorators import authenticated_users

from .forms import LoginForm, SignupForm
from .models import User


@csrf_exempt
@authenticated_users
def user_signup_page(request):
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
                group = Group.objects.get(name="student")
                user.groups.add(group)
            if user_type == "adviser":
                group = Group.objects.get(name="adviser")
                user.groups.add(group)

            messages.success(request, "Successfully registered")
            return redirect("users:login_page")
    else:
        form = SignupForm()

    context = {
        "form": form,
    }
    return render(request, "users/user_signup_page.html", context)


@csrf_exempt
@authenticated_users
def user_login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                if user.groups.filter(name="student"):
                    return redirect("student:home_page")
                if user.groups.filter(name="adviser"):
                    return redirect("adviser:home_page")
                if user.groups.filter(name="admin"):
                    return redirect("administrator:home_page")
            else:
                messages.error(request, "Username and password does not match")
    else:
        form = LoginForm()

    context = {
        "form": form,
    }

    return render(request, "users/user_login_page.html", context)


@csrf_exempt
def user_logout(request):
    logout(request)
    messages.info(request, "User successfully logout")
    return redirect("users:login_page")
