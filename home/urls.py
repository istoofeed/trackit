from django.urls import path

from . import views

app_name = "student"

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("tasks/", views.tasks_page, name="tasks_page"),
    path("task/<int:pk>/", views.task_page, name="task_page"),
    path("upload-file/<int:pk>/", views.upload_file, name="upload_file"),
    path("read-file/<int:pk>/", views.read_taskfile, name="read_file"),
    path(
        "progress/",
        views.capstone_progress_page,
        name="capstone_progress_page",
    ),
    path(
        "progress-tracker/<int:pk>/",
        views.capstone_tracker_page,
        name="capstone_tracker_page",
    ),
    path("advisers/", views.advisers_page, name="advisers_page"),
    path("adviser/<uuid:pk>/", views.adviser_page, name="adviser_page"),
    path(
        "pending-request/<uuid:pk>/",
        views.pending_request_page,
        name="pending_request_page",
    ),
    path(
        "update-pending-request/<int:pk>/",
        views.update_pending_advisory,
        name="update_pending_advisory",
    ),
    path(
        "read-pending-request/<int:pk>/",
        views.read_pending_advisory,
        name="read_pending_advisory",
    ),
    path(
        "read-comment-logs/<int:pk>/",
        views.read_comment_logs,
        name="read_comment_logs",
    ),
    path("capstone-titles/", views.capstone_titles_page, name="capstone_titles_page"),
    path("capstone-group/", views.capstone_group_page, name="capstone_group_page"),
    path("groupchat/", views.groupchat_page, name="groupchat_page"),
    path(
        "read-groupchat-logs/<int:pk>/",
        views.read_groupchat_logs,
        name="read_groupchat_logs",
    ),
    path("profile/", views.profile_page, name="profile_page"),
    path("notifications/", views.notification_page, name="notification_page"),
    path(
        "delete_notification/<int:pk>/",
        views.delete_notification,
        name="delete_notification",
    ),
    path("guides/", views.guides_page, name="guides_page"),
    path("update-profile/", views.update_profile_page, name="update_profile_page"),
    path("read-profile/", views.read_profile_page, name="read_profile_page"),
    path("edit_group/<int:pk>/", views.edit_group, name="edit_group"),
]
