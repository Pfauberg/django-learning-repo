from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import admin
from .views import (
    TaskListCreateAPIView,
    TaskDetailAPIView,
    TaskStatsAPIView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    TaskByWeekdayAPIView,
    CategoryViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
    path('tasks/stats/', TaskStatsAPIView.as_view(), name='task-stats'),
    path('tasks/by-weekday/', TaskByWeekdayAPIView.as_view(), name='tasks-by-weekday'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    path('api/', include(router.urls)),
]
