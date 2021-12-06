from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from account import views as user_views
from django.contrib.auth import views as auth_views
from home import views



urlpatterns = [
    # auth
    path('singup/', user_views.singup, name='singup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    #reset password
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="users/resetpassword.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="users/passwordsent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/passwordresetconfirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="users/passwordresetdone.html"), name='password_reset_complete'),

    # chat
    path('chat/', include('chat.urls')),

    # charsheets
    path('profile/', include('charsheets.urls')),

    # home
    path('', views.home, name='home'),

    # admin
    path('admin/', admin.site.urls),

    # request
    path('request/', include('request.urls')),
]
