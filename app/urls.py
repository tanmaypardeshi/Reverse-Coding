from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('instructions/', views.instructions, name='instructions'),
    path('questions/<int:qno>/', views.questions, name='questions'),
    path('generate/', views.generate, name='generate'),
    path('questions/logout/', views.logout_user, name='logout'),
    path('logout/', views.logout_user, name='logout'),
    path('emergency/', views.emergency, name='emergency'),
    path('ajax/validate_username/', views.validate_username, name='validate_username'),
]