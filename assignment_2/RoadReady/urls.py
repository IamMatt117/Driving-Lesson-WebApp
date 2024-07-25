from django.urls import path
from . import views
from .forms import *


urlpatterns = [
   path('', views.index, name="index"),
   path('login/',views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm)),
   path('logout/', views.logout_user, name="logout"),
   path('register/', views.SignupView.as_view(), name="signup"),
   path('booking/', views.booking, name="booking"),
   path('profile/', views.profile_view, name="profile"),
   path('profile_edit/', views.profile, name="profile_edit"),
   path('password-change/', views.ChangePasswordView.as_view(), name='password_change'),
   path('pricing/', views.pricing, name='pricing'),
   path('checkout/', views.checkout, name='checkout'),
   path('contact/', views.feedback_form, name='contactus'),
   path('timetable/', views.timetable, name="timetable"),
   path('add_to_basket/<int:prodid>/', views.add_to_basket, name='add_to_basket'),
   # The add to basket view at /add_to_basket URL. prodid is a variable part of the URL.
   path('remove_from_basket/<int:item_id>/', views.remove_from_basket, name='remove_from_basket'),
   path('order_complete/<int:order_id>/', views.order_complete, name='order_complete'),
   path('order_history/', views.order_history, name='order_history'),
] 