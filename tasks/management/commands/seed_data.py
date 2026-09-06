from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from tasks.models import User, Project, Tag, Task


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        if User.objects.filter(username='testuser').exists():
            self.stdout.write(self.style.WARNING('Тестовые данные уже существуют. Пропускаем...'))
            return

        self.stdout.write(self.style.SUCCESS('Создание тестовых данных...'))
        self.stdout.write('')

        user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password=make_password('testpass123'),
            settings={'theme': 'light', 'notifications': True},
        )
        self.stdout.write(f'Создан пользователь: {user.username}')

        projects = []
        project_data = [
            ('Личные дела', 'Личные задачи и планы', 'FF5733'),
            ('Работа', 'Рабочие проекты', '33FF57'),
            ('Учеба', 'Курсы и обучение', '3357FF'),
        ]
        for name, desc, color in project_data:
            project = Project.objects.create(
                name=name, description=desc, color=color, owner=user
            )
            projects.append(project)
            self.stdout.write(f'Создан проект: {project.name}')

        tags = []
        for tag_name in ['Важное', 'Срочное', 'Идея', 'Личное', 'Рабочее']:
            tag = Tag.objects.create(name=tag_name, owner=user)
            tags.append(tag)
            self.stdout.write(f'Создан тег: {tag.name}')

        tasks_data = [
            {
                'title': 'Купить продукты',
                'description': 'Молоко, хлеб, яйца, сыр',
                'status': Task.Status.NEW,
                'priority': Task.Priority.MEDIUM,
                'project': projects[0],
                'deadline': timezone.now() + timedelta(days=1),
                'tags': [tags[1], tags[3]],
            },
            {
                'title': 'Сдать отчет',
                'description': 'Подготовить квартальный отчет для начальника',
                'status': Task.Status.IN_PROGRESS,
                'priority': Task.Priority.HIGH,
                'project': projects[1],
                'deadline': timezone.now() + timedelta(hours=5),
                'tags': [tags[0], tags[1], tags[4]],
            },
            {
                'title': 'Прочитать книгу',
                'description': 'Глава 3 "Изучаем Python"',
                'status': Task.Status.NEW,
                'priority': Task.Priority.LOW,
                'project': projects[2],
                'deadline': None,
                'tags': [tags[2], tags[3]],
            },
            {
                'title': 'Позвонить маме',
                'description': '',
                'status': Task.Status.NEW,
                'priority': Task.Priority.MEDIUM,
                'project': None,
                'deadline': timezone.now() + timedelta(days=2),
                'tags': [tags[3]],
            },
        ]

        for task_data in tasks_data:
            tags_list = task_data.pop('tags')
            task = Task.objects.create(user=user, **task_data)
            task.tags.set(tags_list)
            self.stdout.write(f'Создана задача: {task.title}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Успешно создано:'))
        self.stdout.write(f'  пользователей: {User.objects.count()}')
        self.stdout.write(f'  проектов:      {Project.objects.count()}')
        self.stdout.write(f'  тегов:         {Tag.objects.count()}')
        self.stdout.write(f'  задач:         {Task.objects.count()}')