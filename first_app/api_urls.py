from django.urls import path
from .views import (
    TaskCreateAPIView,
    TaskListAPIView,
    TaskDetailAPIView,
    TaskStatsAPIView
)

urlpatterns = [
    path('tasks/create/', TaskCreateAPIView.as_view(), name='task-create'),
    path('tasks/', TaskListAPIView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
    path('tasks/stats/', TaskStatsAPIView.as_view(), name='task-stats'),
]
