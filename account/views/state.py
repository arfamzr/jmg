from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404

from ..models import User


class UserListView(ListView):
    template_name = 'account/state/user/list.html'
    model = User
    paginate_by = 8
    ordering = ['-id']

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            profile__state=self.request.user.profile.state,
            groups__name__in=['Industry'])
        try:
            name = self.request.GET['q']
        except:
            name = ''
        if (name != ''):
            object_list = queryset.filter(username__icontains=name)
        else:
            object_list = queryset
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Senarai Pengguna Sistem'
        return context


def user_detail(request, pk):
    each_user = get_object_or_404(User, pk=pk)

    context = {
        'each_user': each_user,
        'title': 'Maklumat Pengguna',
    }

    return render(request, 'account/state/user/detail.html', context)
