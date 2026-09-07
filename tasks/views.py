from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout

from .models import Task, Project, Tag
from .serializers import (
    TaskSerializer, ProjectSerializer, TagSerializer,
    RegisterSerializer, LoginSerializer, UserSerializer,
)


# Регистрация
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Регистрация успешна',
        })


# Вход
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Вход выполнен',
        })


# Выход
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Выход выполнен'})


# Текущий пользователь
class CurrentUserView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


# Список задач и создание
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Детали, обновление, удаление задачи
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


# Проекты
class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


# Теги
class TagListCreateView(generics.ListCreateAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user)



    