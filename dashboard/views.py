from django.db.models import Q
from django.views.generic import TemplateView
from django.shortcuts import redirect, render

from quarry.models import QuarryMinerData
from mine.models import MineMinerData


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
        quarry_data = QuarryMinerData.objects.all()
        quarry_count = get_counted_data(quarry_data)
        mine_data = MineMinerData.objects.all()
        mine_count = get_counted_data(mine_data)
    elif request.user.is_jmg_state_admin or request.user.is_jmg_state:
        quarry_data = QuarryMinerData.objects.filter(
            state=request.user.profile.state)
        quarry_count = get_counted_data(quarry_data)
        mine_data = MineMinerData.objects.filter(
            state=request.user.profile.state)
        mine_count = get_counted_data(mine_data)
    elif request.user.is_manager:
        quarry_data = QuarryMinerData.objects.filter(miner__miner=request.user)
        quarry_count = get_counted_data(quarry_data)
        mine_data = MineMinerData.objects.filter(miner__miner=request.user)
        mine_count = get_counted_data(mine_data)
    else:
        quarry_count = None
        mine_count = None

    context = {
        'title': 'Dashboard',
        'quarry_count': quarry_count,
        'mine_count': mine_count,
    }
    return render(request, 'dashboard/index.html', context)


class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.request.user.is_industry)
        context["title"] = 'Dashboard'
        return context
