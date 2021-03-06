from django.db.models import Q
from django.views.generic import TemplateView
from django.shortcuts import redirect, render

from quarry.models import Data as QuarryData
from mine.models import Data as MineData
from mineral.models import ProcessData


def get_counted_data(data_list):
    in_process_count = 0
    approved_count = 0
    rejected_count = 0
    draft_count = 0
    for data in data_list:
        approval = data.get_last_approval()
        if approval:
            if approval.state_approved == True and approval.admin_approved == True:
                approved_count += 1
            elif approval.state_approved == False or approval.admin_approved == False:
                rejected_count += 1
            else:
                in_process_count += 1
        else:
            draft_count += 1

    data = {
        'in_process': in_process_count,
        'approved': approved_count,
        'rejected': rejected_count,
        'draft': draft_count,
    }
    return data


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    if request.user.is_jmg_hq:
        quarry_data = QuarryData.objects.all()
        quarry_count = get_counted_data(quarry_data)
        mine_data = MineData.objects.all()
        mine_count = get_counted_data(mine_data)
        mineral_data = ProcessData.objects.all()
        mineral_count = get_counted_data(mineral_data)
    elif request.user.is_jmg_state_admin or request.user.is_jmg_state:
        quarry_data = QuarryData.objects.filter(
            state=request.user.profile.state)
        quarry_count = get_counted_data(quarry_data)
        mine_data = MineData.objects.filter(
            state=request.user.profile.state)
        mine_count = get_counted_data(mine_data)
        mineral_data = ProcessData.objects.filter(
            state=request.user.profile.state)
        mineral_count = get_counted_data(mineral_data)
    elif request.user.is_manager:
        quarry_data = QuarryData.objects.filter(manager__user=request.user)
        quarry_count = get_counted_data(quarry_data)
        mine_data = MineData.objects.filter(manager__user=request.user)
        mine_count = get_counted_data(mine_data)
        mineral_data = ProcessData.objects.filter(manager__user=request.user)
        mineral_count = get_counted_data(mineral_data)
    elif request.user.is_super_admin:
        return redirect('account:super_admin:hq_list')
    else:
        quarry_count = None
        mine_count = None

    context = {
        'title': 'Papan Pemuka',
        'quarry_count': quarry_count,
        'mine_count': mine_count,
        'mineral_count': mineral_count,
    }
    return render(request, 'dashboard/index.html', context)


class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.request.user.is_industry)
        context["title"] = 'Dashboard'
        return context
