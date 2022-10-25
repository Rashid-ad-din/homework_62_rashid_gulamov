from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from webapp.forms import SearchForm
from webapp.forms import TaskForm
from webapp.models import Task, Project


class GroupPermission(UserPassesTestMixin):
    groups = []

    def test_func(self):
        return self.request.user.groups.filter(name__in=self.groups).exists()


class SuccessDetailUrlMixin:
    def get_success_url(self):
        return reverse('show_task', kwargs={'pk': self.object.pk})


class AddTaskView(GroupPermission, SuccessDetailUrlMixin, LoginRequiredMixin, CreateView):
    template_name = 'tasks/add_task.html'
    form_class = TaskForm
    model = Task
    extra_context = ()
    groups = ['admin', 'Project Manager', 'Team Lead', 'Developer']

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        form.instance.project = project
        return super().form_valid(form)


class TasksView(ListView):
    template_name = 'tasks/tasks.html'
    model = Task
    context_object_name = 'tasks'
    queryset = Task.objects.without_deleted()
    paginate_by = 10
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')
        return None

    def get_queryset(self):
        queryset = super().get_queryset().all()
        if self.search_value:
            query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context


class TaskView(DetailView):
    template_name = 'tasks/task.html'
    model = Task

    def get_object(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        task = get_object_or_404(Task, pk=pk)

        if task.is_deleted:
            raise Http404('Task not found/deleted')
        return task


class TaskUpdateView(GroupPermission, SuccessDetailUrlMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tasks/edit_task.html'
    form_class = TaskForm
    model = Task
    groups = ['admin', 'Project Manager', 'Team Lead', 'Developer']


class TaskDeleteView(GroupPermission, DeleteView, LoginRequiredMixin):
    template_name = 'tasks/delete.html'
    model = Task
    success_url = reverse_lazy('show_projects')
    groups = ['admin', 'Project Manager', 'Team Lead', 'Developer']

