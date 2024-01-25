from django.urls import path

from . import views

app_name = "adviser"

urlpatterns = [
    path("home/", views.home_page, name="home_page"),
    path("tasks/", views.tasks_page, name="tasks_page"),
    path("users-tasks/<int:pk>", views.users_tasks_page, name="users_tasks_page"),
    path("need_revision/<int:pk>", views.need_revision, name="need_revision"),
    path(
        "usertask/<int:pk>", views.usertask_details_page, name="usertask_details_page"
    ),
    # ? Create Task Pages
    path("create-task-page/", views.create_task_page, name="create_task_page"),
    path("update-task-page/<int:pk>/", views.update_task_page, name="update_task_page"),
    path("delete-task-page/<int:pk>/", views.delete_task, name="delete_task"),
    # ? Announcement Pages
    path(
        "create-announcement-page/",
        views.create_announcement_page,
        name="create_announcement_page",
    ),
    path(
        "update-announcement-page/<int:pk>/",
        views.update_announcement_page,
        name="update_announcement_page",
    ),
    path(
        "delete-announcement/<int:pk>/",
        views.delete_announcement,
        name="delete_announcement",
    ),
    # Tracker
    path(
        "capstone-progress-tracker/<int:pk>/",
        views.capstone_progress_tracker_page,
        name="capstone_progress_tracker_page",
    ),
    path(
        "capstone-progress/<int:pk>/",
        views.capstone_progress,
        name="capstone_progress",
    ),
    path(
        "first_section_done/<int:pk>/",
        views.first_section_done,
        name="first_section_done",
    ),
    path(
        "last_section_done/<int:pk>/",
        views.last_section_done,
        name="last_section_done",
    ),
    path(
        "section_done/<int:pk>/",
        views.section_done,
        name="section_done",
    ),
    path("advisories/", views.advisories_page, name="advisories_page"),
    path(
        "advisory-group-details/",
        views.advisory_group_details_page,
        name="advisory_group_details_page",
    ),
    path(
        "capstone-approved-titles/",
        views.capstone_approved_titles_page,
        name="capstone_approved_titles_page",
    ),
    path(
        "capstone-group-requests/",
        views.capstone_group_requests_page,
        name="capstone_group_requests_page",
    ),
    path(
        "requests-details/<int:pk>/",
        views.request_details_page,
        name="request_details_page",
    ),
    path(
        "read-comment-logs/<int:pk>/",
        views.read_comment_logs,
        name="read_comment_logs",
    ),
    path(
        "read-groupchat-logs/<int:pk>/",
        views.read_groupchat_logs,
        name="read_groupchat_logs",
    ),
    path("reject-request/<int:pk>/", views.reject_request, name="reject_request"),
    path("accept-request/<int:pk>/", views.accept_request, name="accept_request"),
    path("groupchat/<int:pk>/", views.groupchat_page, name="groupchat_page"),
    path("profile/", views.profile_page, name="profile_page"),
    path("update-profile/", views.update_profile_page, name="update_profile_page"),
    path("read-profile/", views.read_profile_page, name="read_profile_page"),
    path("notifications/", views.notification_page, name="notification_page"),
    path(
        "delete_notification/<int:pk>/",
        views.delete_notification,
        name="delete_notification",
    ),
    path("guides/", views.guides, name="guides"),
]
