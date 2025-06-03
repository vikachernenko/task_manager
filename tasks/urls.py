from django.urls import path
from . import views
from .views import daily_tasks

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('criteria/', views.criteria_list, name='criteria_list'),
    path('criteria/create/', views.criteria_create, name='criteria_create'),
    path('criteria/<int:criteria_id>/', views.task_list, name='task_list'),
    path('tasks/', views.task_list_simple,
         name='task_list_simple'),  # Новый маршрут
    path('criteria/<int:criteria_id>/create/',
         views.task_create, name='task_create'),
    path('task/<int:task_id>/update/', views.task_update, name='task_update'),
    path('task/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('notifications/', views.notifications, name='notifications'),
    path('criteria/<int:criteria_id>/delete/',
         views.criteria_delete, name='criteria_delete'),
    path('daily/', daily_tasks, name='daily_tasks'),
]
