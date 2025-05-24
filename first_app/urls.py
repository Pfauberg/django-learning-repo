from django.urls import path
from . import views
from .views import RegisterView
from .views import LogoutView

urlpatterns = [
    path('hello/', views.hello_view, name='hello'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
