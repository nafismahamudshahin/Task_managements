from django.urls import path
from django.contrib.auth.views import LogoutView , PasswordChangeView
from django.views.generic import TemplateView
from users.views import sign_up ,sign_in ,ProfileView,CustomLoginView, EditProfileView , CustomPasswordChangeView,PasswordResetView,CustomPasswordResetConfirmView, sign_out ,activateUser ,admin_dashboard ,assign_role , create_group , group_list , task_details
urlpatterns = [
    path('sign-up/',sign_up,name="sign-up"),
    path('sign-in/',CustomLoginView.as_view(),name="sign-in"),
    path('sign-out/',LogoutView.as_view(),name="sign-out"),
    path('activate/<int:id>/<str:token>/', activateUser),
    path("admin-dashboard/",admin_dashboard,name="admin-dashboard"),
    path("assign-role/<int:id>/",assign_role,name="assign-role"),
    path('create-group/',create_group,name="create-group"),
    path('group-list/',group_list,name="group-list"),
    path('task-details/',task_details,name="task-details"),
    path('change-password/',CustomPasswordChangeView.as_view(),name="change-password"),
    path('profile/',ProfileView.as_view(),name="profile"),
    path('password-reset/',PasswordResetView.as_view() , name="password-reset"),
    path('confirm-password-reset/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view() , name="password_reset_confirm"),
    path('edit-profile/', EditProfileView.as_view(),name="edit_profile"),
]
