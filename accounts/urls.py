from django.urls import path, include
from .views import login
from .views import logout
from .views import password_reset_request
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('password_reset/', password_reset_request, name='password_reset'),  
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),  
]
