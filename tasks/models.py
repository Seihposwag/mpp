from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class User(AbstractUser):
    """Пользователь, расширяет встроенную модель Django"""
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    settings = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'


class Project(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3, 'Название должно содержать минимум 3 символа')]
    )
    description = models.TextField(blank=True, null=True)
    color = models.CharField(
        max_length=7,
        default='808080',
        validators=[RegexValidator(
            regex='^([A-Fa-f0-9]{6})$',
            message='Цвет должен быть в формате HEX (RRGGBB)'
        )]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'projects'
        unique_together = ['name', 'owner']


class Tag(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'
        unique_together = ['name', 'owner']


class Task(models.Model):
    class Status(models.TextChoices):
        NEW = 'New', 'Новая'
        IN_PROGRESS = 'InProgress', 'В работе'
        COMPLETED = 'Completed', 'Выполнена'

    class Priority(models.TextChoices):
        LOW = 'Low', 'Низкий'
        MEDIUM = 'Medium', 'Средний'
        HIGH = 'High', 'Высокий'

    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(3, 'Заголовок должен содержать минимум 3 символа')]
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    tags = models.ManyToManyField(Tag, through='TaskTag', related_name='tasks')

    def clean(self):
        """Кастомная валидация"""
        if self.deadline and self.deadline.date() < timezone.now().date():
            raise ValidationError({'deadline': 'Дедлайн не может быть в прошлом'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tasks'
        ordering = ['-created_at']


class TaskTag(models.Model):
    """Промежуточная модель для связи Task и Tag"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task_tags'
        unique_together = ['task', 'tag']