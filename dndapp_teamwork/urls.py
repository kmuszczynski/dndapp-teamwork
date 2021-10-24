from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from charsheets import views

urlpatterns = [
    # auth
    # TODO: Move auth stuff out of the charsheets.views a into their own app or something
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),

    # chat
    path('chat/', include('chat.urls')),

    # charsheets
    path('charsheets/', include('charsheets.urls')),

    # admin
    path('admin/', admin.site.urls),
]
