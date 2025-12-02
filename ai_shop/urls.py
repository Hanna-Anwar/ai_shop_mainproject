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

from django.urls import path,include

from django.conf import settings

from django.conf.urls.static import static


from user_app.views import *

from product_app.views import *

from cart_app.views import *

from wishlist_app.views import *

urlpatterns = [

    path('admin/', admin.site.urls),

    #user_app/urls

    path('register/',UserRegisterView.as_view(),name="register"),

    path('',HomeView.as_view(),name="home"),

     path('login/',LoginView.as_view(),name="login"),

     path('logout/',LogoutView.as_view(),name="logout"),

     path('forgetmail/',ForgetEmailView.as_view(),name="forget"),

    path('otpverify/',OtpVerifyView.as_view(),name="otp"),

    path('resetpassword/',PasswordResetView.as_view(),name="reset"),

    path('profilecreate/',UserProfileView.as_view(),name="profile_create"),

    path('profileshow/',ProfileShowView.as_view(),name="profile_show"),

    path('profileedit/',ProfileEditView.as_view(),name="profile_edit"),

    #product_app/urls

    path('products/', ProductListView.as_view(), name='product_list'), 

    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),  # Detail page

    #cart_app/urls

    path('addtocart/<int:pk>',AddToCartView.as_view(),name="add_to_cart"),

    path('cart/',CartDetailView.as_view(),name="cart_details"),

    path('cart_increase/<int:pk>',CartIncreaseView.as_view(),name="cart_increase"),

    path('cart_decrease/<int:pk>',CartDecreaseView.as_view(),name="cart_decrease"),
    
    path('remove_cart/<int:pk>',CartRemoveView.as_view(),name="cart_remove"),

    # wishlist_app/urls

    path('addtowishlist/<int:pk>',AddToWishlistView.as_view(),name="add_wishlist"),

    path('list_wishlist/',WishlistDetailView.as_view(),name="wishlist_details"),

    path('remove_wishlist/<int:pk>',WishlistRemoveView.as_view(),name="wishlist_remove"),


]


if settings.DEBUG:
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

