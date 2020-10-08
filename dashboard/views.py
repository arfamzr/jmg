from django.views.generic import TemplateView
from django.shortcuts import render


class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.request.user.is_industry)
        context["title"] = 'Dashboard'
        return context
