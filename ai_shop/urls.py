"""
URL configuration for ai_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from user_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/',UserRegisterView.as_view(),name="register"),

    path('',HomeView.as_view(),name="home"),

     path('login/',LoginView.as_view(),name="login"),

     path('logout/',LogoutView.as_view(),name="logout"),

     path('forgetmail/',ForgetEmailView.as_view(),name="forget"),

    path('otpverify/',OtpVerifyView.as_view(),name="otp"),

    path('resetpassword/',PasswordResetView.as_view(),name="reset"),

    path('profile/',UserProfileView.as_view(),name="profile"),
]
