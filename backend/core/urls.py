from django.urls import path

from .views import (
    GroupDetailAPIView,
    GroupListCreateAPIView,
    join_group,
    leave_group,
    login_view,
    register_view,
    logout_view,
    remove_member,
    subject_list,
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("subjects/", subject_list, name="subject-list"),
    path("groups/", GroupListCreateAPIView.as_view(), name="group-list"),
    path("groups/<int:pk>/", GroupDetailAPIView.as_view(), name="group-detail"),
    path("groups/<int:pk>/join/", join_group, name="join-group"),
    path("groups/<int:pk>/leave/", leave_group, name="leave-group"),
    path("groups/<int:pk>/remove-member/", remove_member, name="remove-member"),
]
