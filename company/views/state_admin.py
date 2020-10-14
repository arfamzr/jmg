from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from account.models import User

from ..models import Company
from ..forms import CompanyForm


class CompanyListView(ListView):
    template_name = 'company/state_admin/list.html'
    model = Company
    paginate_by = 8
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            state=self.request.user.profile.state)
        try:
            name = self.request.GET['q']
        except:
            name = ''
        if (name != ''):
            object_list = queryset.filter(name__icontains=name)
        else:
            object_list = queryset
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Senarai Syarikat'
        return context


class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/state_admin/form.html'
    success_url = reverse_lazy('company:state_admin:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Syarikat'
        return context


class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/state_admin/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update Syarikat'
        return context


def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    user_list = User.objects.all().filter(employee__company=company)

    try:
        name = request.GET['q']
    except:
        name = ''
    if (name != ''):
        user_list = user_list.filter(username__icontains=name)

    context = {
        'company': company,
        'user_list': user_list,
        'title': 'Maklumat Syarikat',
    }

    return render(request, 'company/state_admin/detail.html', context)


def add_employee(request, pk):
    company = get_object_or_404(Company, pk=pk)
    user_list = User.objects.all().filter(
        profile__state=request.user.profile.state,
        groups__name__in=['Industry']).exclude(employee__company=company)

    try:
        name = request.GET['q']
    except:
        name = ''
    if (name != ''):
        user_list = user_list.filter(username__icontains=name)

    context = {
        'company': company,
        'user_list': user_list,
        'title': f'Tambah pekerja "{company.name}"',
    }

    return render(request, 'company/state_admin/add_user.html', context)
