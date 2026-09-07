from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Аутентификация
    path('api/auth/register/', views.RegisterView.as_view(), name='register'),
    path('api/auth/login/', views.LoginView.as_view(), name='login'),
    path('api/auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('api/auth/me/', views.CurrentUserView.as_view(), name='current-user'),

    # Задачи
    path('api/tasks/', views.TaskListCreateView.as_view(), name='task-list'),
    path('api/tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),

    # Проекты
    path('api/projects/', views.ProjectListCreateView.as_view(), name='project-list'),
    path('api/projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),

    # Теги
    path('api/tags/', views.TagListCreateView.as_view(), name='tag-list'),
    path('api/tags/<int:pk>/', views.TagDetailView.as_view(), name='tag-detail'),

        # JWT-токены
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]




