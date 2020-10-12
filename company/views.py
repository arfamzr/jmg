from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import ( 
    Company 
)

from .forms import (
    CompanyForm
)


class CompanyListView(ListView):
    template_name = 'company/list.html'
    model = Company
    paginate_by = 8
    ordering = ['id']

    def get_queryset(self):
        try:
            name = self.request.GET['q']
        except:
            name = ''
        if (name != ''):
            object_list = self.model.objects.filter(company_name__icontains=name)
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Syarikat'
        return context

class CompanyCreateView(CreateView):
    template_name = 'company/form.html'
    model = Company
    form_class = CompanyForm
    success_url = reverse_lazy('company:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tambah Syarikat'
        return context

class CompanyUpdate(UpdateView):
    template_name = 'company/form.html'
    model = Company
    form_class = CompanyForm
    success_url = reverse_lazy('company:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Kemaskini Syarikat'
        return context

class CompanyDetail(DetailView):
    template_name = 'company/detail.html'
    model = Company
    context_object_name = 'company'