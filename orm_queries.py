# python orm_queries.py

from datetime import timedelta
from django.utils import timezone
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from first_app.models import Task, SubTask

now = timezone.now()

task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status="new",
    deadline=now + timedelta(days=3)
)

subtask1 = SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    status="new",
    deadline=now + timedelta(days=2),
    task=task
)

subtask2 = SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    status="new",
    deadline=now + timedelta(days=1),
    task=task
)

print(Task.objects.filter(status="new"))

print(SubTask.objects.filter(status="done", deadline__lt=timezone.now()))

task.status = "in_progress"
task.save()

subtask1.deadline = now - timedelta(days=2)
subtask1.save()

subtask2.description = "Create and format presentation slides"
subtask2.save()

# task.delete()
