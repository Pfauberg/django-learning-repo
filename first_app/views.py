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


from rest_framework import status
from .models import SubTask
from .serializers import SubTaskCreateSerializer


class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskCreateSerializer(subtasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
