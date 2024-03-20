from django.urls import path
from .views import *
urlpatterns = [
    path('',List.as_view(),name='home'),
    path('detail/<slug:slug>',detailView,name='detailView'),
    path('', index,name='index'),
    path('register/', register,name='register'),
    path('login/', logIn,name='login'),
    path('logout/',logOut,name='logout' ),
    path('post_detail/',detailView,name='post_detail' )
    ]