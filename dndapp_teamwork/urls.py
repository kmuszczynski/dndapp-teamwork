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

    # chat
    path('chat/', include('chat.urls')),

    # charsheets
    path('profile/', include('charsheets.urls')),

    # home
    path('', views.home, name='home'),

    # admin
    path('admin/', admin.site.urls),
]
