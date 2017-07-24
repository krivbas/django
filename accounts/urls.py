from django.conf.urls import url

from accounts.views import sign_in, sign_out, get_user_django, get_user_rest, change_user_password, \
    ChangeUserPasswordView

urlpatterns = [
    url(r'^sign-in/$', sign_in, name='sign_in'),
    url(r'^sign-out/$', sign_out, name='sign_out'),
    url(r'^get-user-django/$', get_user_django, name='get_user_django'),
    url(r'^get-user-rest/$', get_user_rest),
    url(r'^change-user-password/$', change_user_password),
    url(r'^change-user-password-rest/$', ChangeUserPasswordView.as_view()),
]