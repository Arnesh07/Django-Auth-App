from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view()),
    path('oauth/', views.LoginView.as_view()),
    path('home/', views.HomePageView.as_view()),
]
