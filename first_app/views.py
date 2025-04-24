from django.http import HttpResponse

def hello_view(request):
    your_name = "JOHN"
    return HttpResponse(f"<h1>Hello, {your_name}</h1>")

from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from .models import Task, SubTask
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskCreateSerializer
)

class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all().order_by('-created_at')
    serializer_class = SubTaskCreateSerializer
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']


class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer


class TaskStatsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        total = Task.objects.count()
        by_status = Task.objects.values('status').annotate(count=Count('id'))
        overdue = Task.objects.filter(deadline__lt=timezone.now()).count()
        return Response({
            "total_tasks": total,
            "tasks_by_status": by_status,
            "overdue_tasks": overdue
        })


class TaskByWeekdayAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        weekday_param = self.request.query_params.get('weekday')
        if weekday_param:
            try:
                weekday_number = {
                    "понедельник": 0,
                    "вторник": 1,
                    "среда": 2,
                    "четверг": 3,
                    "пятница": 4,
                    "суббота": 5,
                    "воскресенье": 6
                }[weekday_param.lower()]
                queryset = queryset.filter(deadline__week_day=weekday_number + 1)
            except KeyError:
                pass
        return queryset
