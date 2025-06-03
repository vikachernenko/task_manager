from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Criteria, Task
from .forms import TaskForm, CriteriaForm
from django.utils import timezone


def welcome(request):
    first_criteria_id = Criteria.objects.first(
    ).id if Criteria.objects.exists() else None
    return render(request, 'tasks/welcome.html', {'first_criteria_id': first_criteria_id})


@login_required
def criteria_list(request):
    criteria = Criteria.objects.all()
    return render(request, 'tasks/criteria_list.html', {'criteria': criteria})


@login_required
def criteria_create(request):
    if request.method == 'POST':
        form = CriteriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('criteria_list')
    else:
        form = CriteriaForm()
    return render(request, 'tasks/criteria_form.html', {'form': form})


@login_required
def task_list(request, criteria_id):
    criteria = get_object_or_404(Criteria, id=criteria_id)
    tasks = Task.objects.filter(criterion=criteria)
    status_filter = request.GET.get('status', '')
    if status_filter:
        tasks = tasks.filter(criterion__status=status_filter)
    return render(request, 'tasks/task_list.html', {'criteria': criteria, 'tasks': tasks})


@login_required
def task_list_simple(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list_simple.html', {'tasks': tasks})


@login_required
def task_create(request, criteria_id):
    criteria = get_object_or_404(Criteria, id=criteria_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.criterion = criteria
            task.user = request.user
            task.save()
            return redirect('task_list', criteria_id=criteria.id)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'criteria': criteria})


@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list', criteria_id=task.criterion.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'criteria': task.criterion})


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    criteria_id = task.criterion.id
    task.delete()
    return redirect('task_list', criteria_id=criteria_id)


@login_required
def notifications(request):
    threshold_24h = timezone.now() + timedelta(hours=24)
    urgent_tasks = Task.objects.filter(
        deadline__lte=threshold_24h,
        deadline__gte=timezone.now(),
        user=request.user
    )
    return render(request, 'tasks/notifications.html', {'urgent_tasks': urgent_tasks})


@login_required
def criteria_delete(request, criteria_id):
    criteria = get_object_or_404(Criteria, id=criteria_id)

    # Проверяем, есть ли связанные задачи
    if criteria.task_set.exists():
        messages.error(request, 'Нельзя удалить категорию с задачами')
    else:
        criteria.delete()
        messages.success(request, 'Категория успешно удалена')

    return redirect('criteria_list')


@login_required
def daily_tasks(request):
    today = datetime.now().date()
    day_offset = int(request.GET.get('day', 0))
    target_date = today + timedelta(days=day_offset)
    end_date = target_date + timedelta(days=10)  # Добавляем 10 дней

    # Получаем задачи для 10-дневного периода
    tasks = Task.objects.filter(
        user=request.user,
        deadline__date__gte=target_date,
        deadline__date__lte=end_date
    ).order_by('deadline')

    # Создаем список дней с задачами
    days = []
    for i in range(11):  # 10 дней + текущий день
        current_day = target_date + timedelta(days=i)
        days.append({
            'date': current_day,
            'tasks': [t for t in tasks if t.deadline.date() == current_day]
        })

    context = {
        'days': days,
        'current_date': target_date,
        'today': today,
        'day_offset': day_offset,
    }
    return render(request, 'tasks/daily_tasks.html', context)
