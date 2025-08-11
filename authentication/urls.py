from django.urls import path
from authentication.views import RegisterView
from django.contrib.auth import views as auth_views
from authentication import views

urlpatterns = [
    path("register/", RegisterView.as_view(), name='register'),

    path(
        "accounts/password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",  # the form template
            email_template_name="registration/password_reset_email.html",  # the HTML email template
            subject_template_name="registration/password_reset_subject.txt",  # optional subject
            html_email_template_name="registration/password_reset_email.html",  # this is important!
        ),
        name="password_reset",  # place this outside the as_view()
    ),

    path("change-password/", views.user_change_pass, name='changepass'),
    path("profile/", views.user_profile, name='profile'),



]