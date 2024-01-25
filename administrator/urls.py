from django.urls import path

from . import views

app_name = "administrator"

urlpatterns = [
    path("", views.home_page, name="home_page"),
    #! Task
    path("create-task-page/", views.create_task_page, name="create_task_page"),
    path("update-task-page/<int:pk>/", views.update_task_page, name="update_task_page"),
    path("delete-task-page/<int:pk>/", views.delete_task, name="delete_task"),
    #! Announcement
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
    path(
        "capstone-progress-tracker/",
        views.capstone_progress_tracker_page,
        name="capstone_progress_tracker_page",
    ),
    path(
        "capstone-progress/<int:pk>/",
        views.capstone_progress,
        name="capstone_progress",
    ),
    path(
        "capstone-tracker/<int:pk>/",
        views.capstone_tracker,
        name="capstone_tracker",
    ),
    #! Advisories
    path("advisories", views.advisories_page, name="advisories_page"),
    path(
        "create-groupadvisory-page/",
        views.create_groupadvisory_page,
        name="create_groupadvisory_page",
    ),
    path(
        "update-groupadvisory-page/<int:pk>/",
        views.update_groupadvisory_page,
        name="update_groupadvisory_page",
    ),
    path(
        "delete-groupadvisory/<int:pk>/",
        views.delete_groupadvisory,
        name="delete_groupadvisory",
    ),
    #! Approved Title
    path(
        "approved-capstone-titles/",
        views.approved_capstone_titles_page,
        name="approved_capstone_titles_page",
    ),
    path(
        "create-approvedtitle-page/",
        views.create_approved_title_page,
        name="create_approved_title_page",
    ),
    path(
        "update-approvedtitle-page/<int:pk>/",
        views.update_approved_title_page,
        name="update_approved_title_page",
    ),
    path(
        "delete-approvedtitle/<int:pk>/",
        views.delete_approved_title,
        name="delete_approved_title",
    ),
    path("groupchat/", views.groupchat_page, name="groupchat_page"),
    path("capstone-group/", views.capstone_group_page, name="capstone_group_page"),
    path("add_users/", views.add_users, name="add_users"),
    path("delete_user/<uuid:pk>/", views.delete_user, name="delete_user"),
    path("users/", views.users_page, name="users_page"),
    path("users/advisers", views.advisers_page, name="advisers_page"),
    path(
        "create-groupings/",
        views.create_groupings,
        name="create_groupings",
    ),
    path("delete-groupings/", views.delete_all_groups, name="delete_all_groups"),
    path("guides/", views.guides, name="guides"),
    path("add_guide/", views.add_guide, name="add_guide"),
    path("edit_guide/<int:pk>/", views.edit_guide, name="edit_guide"),
    path("delete_guide/<int:pk>/", views.delete_guide, name="delete_guide"),
    path("approved_group/<int:pk>/", views.approved_group, name="approved_group"),
    path("delete_group/<int:pk>/", views.delete_group, name="delete_group"),
    path(
        "approved_group_page/",
        views.approved_group_page,
        name="approved_group_page",
    ),
]
