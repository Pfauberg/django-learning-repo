from django.http import HttpResponse

def hello_view(request):
    your_name = "JOHN"
    return HttpResponse(f"<h1>Hello, {your_name}</h1>")


from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Count, Q
from .models import Task
from .serializers import TaskSerializer


class TaskCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailAPIView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


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
