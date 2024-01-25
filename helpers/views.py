from django.shortcuts import render


def not_found_page(request, exception):
    return render(request, "404_page.html")


def server_error_page(request):
    return render(request, "server_error_page.html")
