from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from ..models import Company, Employee


class CompanyListView(ListView):
    template_name = 'company/state/list.html'
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

    return render(request, 'company/state/detail.html', context)
