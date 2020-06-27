from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('user/', views.UserView.as_view()),
    path('notices/', views.NoticesView.as_view()),
    path('notice/<int:notice_id>/', views.NoticeView.as_view()),
    path('quote/', views.QuoteView.as_view())
]
