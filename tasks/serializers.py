from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import Task, Project, Tag

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar', 'created_at')
        read_only_fields = ('id', 'created_at')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError('Неверный логин или пароль')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'color', 'created_at')
        read_only_fields = ('id', 'created_at')


class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), source='project',
        write_only=True, required=False, allow_null=True
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), source='tags',
        write_only=True, many=True, required=False
    )

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'created_at', 'deadline',
                  'status', 'priority', 'project', 'project_id', 'tags', 'tag_ids')
        read_only_fields = ('id', 'created_at')