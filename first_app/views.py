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


from rest_framework import generics
from .models import SubTask
from .serializers import SubTaskCreateSerializer


class SubTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = SubTaskCreateSerializer

    def get_queryset(self):
        queryset = SubTask.objects.all().order_by('-created_at')
        task_title = self.request.query_params.get('task')
        status_param = self.request.query_params.get('status')

        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)
        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset


class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return None

    def get(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({"error": "Not found"}, status=404)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({"error": "Not found"}, status=404)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({"error": "Not found"}, status=404)
        subtask.delete()
        return Response(status=204)


from rest_framework import generics
from .serializers import TaskSerializer


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
