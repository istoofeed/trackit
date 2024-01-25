from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse


def authenticated_users(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                if group == "admin":
                    previous_url = reverse("administrator:home_page")
                if group == "adviser":
                    previous_url = reverse("adviser:home_page")
                if group == "student":
                    previous_url = reverse("student:home_page")
                return render(
                    request,
                    "403_access_denied_page.html",
                    {"previous_url": previous_url},
                )

        return wrapper_func

    return decorator


def students_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None

        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == "admin":
                return redirect("administrator:home_page")
            if group == "adviser":
                return redirect("adviser:home_page")
            if group == "student":
                return view_func(request, *args, **kwargs)
            if group == "":
                return view_func(request, *args, **kwargs)
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
