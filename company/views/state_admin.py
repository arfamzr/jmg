from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from account.models import User

from ..models import Company, Employee
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

    def form_valid(self, form):
        form.instance.state = self.request.user.profile.state
        return super().form_valid(form)

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
    employee_list = Employee.objects.filter(company=company)

    try:
        name = request.GET['q']
    except:
        name = ''
    if (name != ''):
        employee_list = employee_list.filter(user__username__icontains=name)

    context = {
        'company': company,
        'employee_list': employee_list,
        'title': 'Maklumat Syarikat',
    }

    return render(request, 'company/state_admin/detail.html', context)


def toggle_active(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        if company.status == True:
            company.status = False
        else:
            company.status = True
        company.save()
        return redirect('company:state_admin:list')

    context = {
        'company': company,
    }

    return render(request, 'company/state_admin/toggle_active.html', context)


def add_employee(request, pk):
    company = get_object_or_404(Company, pk=pk)
    user_list = User.objects.all().filter(
        groups__name__in=['Industry'],
        employee__company=None)

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


def company_add_employee(request, company_pk, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    company = get_object_or_404(Company, pk=company_pk)

    employee, created = Employee.objects.get_or_create(
        user=user,
    )

    employee.company = company
    employee.add_by = request.user
    employee.save()

    return redirect('company:state_admin:detail', company.pk)


def company_remove_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    company_pk = employee.company.pk
    employee.delete()

    return redirect('company:state_admin:detail', company_pk)
