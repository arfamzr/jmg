from django.shortcuts import render
from django.db.models import Sum

from quarry.models import QuarryDataApproval

from ..forms.hq import GraphForm


def quarry_graph(request):
    form = GraphForm(request.GET)
    if form.is_valid():
        year = form.cleaned_data.get('year')
        month = form.cleaned_data.get('month')
        rock_type1 = form.cleaned_data.get('rock_type1')
        rock_type2 = form.cleaned_data.get('rock_type2')
        rock_type3 = form.cleaned_data.get('rock_type3')
        rock_type4 = form.cleaned_data.get('rock_type4')
        rock_type5 = form.cleaned_data.get('rock_type5')

        rock_list = QuarryDataApproval.objects.filter(miner_data__year=year)
        if month:
            rock_list.filter(miner_data__month=month)

        rock1_list = rock_list.filter(
            miner_data__quarry__main_rock_type=rock_type1)
        rock2_list = rock_list.filter(
            miner_data__quarry__main_rock_type=rock_type2)
        rock3_list = rock_list.filter(
            miner_data__quarry__main_rock_type=rock_type3)
        rock4_list = rock_list.filter(
            miner_data__quarry__main_rock_type=rock_type4)
        rock5_list = rock_list.filter(
            miner_data__quarry__main_rock_type=rock_type5)

        rock1_perlis_list = rock1_list.filter(miner_data__quarry__state='PLS')
        rock1_perlis_production = 0
        rock1_perlis_royalties = 0
        for rock in rock1_perlis_list:
            rock1_perlis_production += rock.miner_data.productionstatistic.main_rock_production
            rock1_perlis_royalties += rock.miner_data.royalties.royalties

        rock1_kedah_list = rock1_list.filter(miner_data__quarry__state='KDH')
        rock1_kedah_production = 0
        rock1_kedah_royalties = 0
        for rock in rock1_kedah_list:
            rock1_kedah_production += rock.miner_data.productionstatistic.main_rock_production
            rock1_kedah_royalties += rock.miner_data.royalties.royalties

        rock1_penang_list = rock1_list.filter(miner_data__quarry__state='PNG')
        rock1_penang_production = 0
        rock1_penang_royalties = 0
        for rock in rock1_penang_list:
            rock1_penang_production += rock.miner_data.productionstatistic.main_rock_production
            rock1_penang_royalties += rock.miner_data.royalties.royalties

        rock1_perak_list = rock1_list.filter(miner_data__quarry__state='PRK')
        rock1_perak_production = 0
        rock1_perak_royalties = 0
        for rock in rock1_perak_list:
            rock1_perak_production += rock.miner_data.productionstatistic.main_rock_production
            rock1_perak_royalties += rock.miner_data.royalties.royalties

        rock1_selangor_list = rock1_list.filter(
            miner_data__quarry__state='SGR')
        rock1_selangor_production = 0
        rock1_selangor_royalties = 0
        for rock in rock1_selangor_list:
            rock1_selangor_production += rock.miner_data.productionstatistic.main_rock_production
            rock1_selangor_royalties += rock.miner_data.royalties.royalties

        rock1_nsembilan_list = rock1_list.filter(
            miner_data__quarry__state='PLS')
        rock1_nsembilan_production = 0
        rock1_nsembilan_royalties = 0
        for rock in rock1_nsembilan_list:
            rock1_nsembilan_production += rock.miner_data.productionstatistic.main_rock_production
            rock1_nsembilan_royalties += rock.miner_data.royalties.royalties

        rock1_melaka_list = rock1_list.filter(miner_data__quarry__state='MLK')
        rock1_melaka_production = 0
        rock1_melaka_royalties = 0
        for rock in rock1_melaka_list:
            rock1_melaka_production += rock.miner_data.productionstatistic.main_rock_production
            rock1_melaka_royalties += rock.miner_data.royalties.royalties

        rock1_johor_list = rock1_list.filter(miner_data__quarry__state='JHR')
        rock1_johor_production = 0
        rock1_johor_royalties = 0
        for rock in rock1_johor_list:
            rock1_johor_production += rock.miner_data.productionstatistic.main_rock_production
            rock1_johor_royalties += rock.miner_data.royalties.royalties

        rock1_pahang_list = rock1_list.filter(miner_data__quarry__state='PHG')
        rock1_pahang_production = 0
        rock1_pahang_royalties = 0
        for rock in rock1_pahang_list:
            rock1_pahang_production += rock.miner_data.productionstatistic.main_rock_production
            rock1_pahang_royalties += rock.miner_data.royalties.royalties

        rock1_terengganu_list = rock1_list.filter(
            miner_data__quarry__state='TRG')
        rock1_terengganu_production = 0
        rock1_terengganu_royalties = 0
        for rock in rock1_terengganu_list:
            rock1_terengganu_production += rock.miner_data.productionstatistic.main_rock_production
            rock1_terengganu_royalties += rock.miner_data.royalties.royalties

        rock1_kelantan_list = rock1_list.filter(
            miner_data__quarry__state='KTN')
        rock1_kelantan_production = 0
        rock1_kelantan_royalties = 0
        for rock in rock1_kelantan_list:
            rock1_kelantan_production += rock.miner_data.productionstatistic.main_rock_production
            rock1_kelantan_royalties += rock.miner_data.royalties.royalties

        rock1_sarawak_list = rock1_list.filter(miner_data__quarry__state='SWK')
        rock1_sarawak_production = 0
        rock1_sarawak_royalties = 0
        for rock in rock1_sarawak_list:
            rock1_sarawak_production += rock.miner_data.productionstatistic.main_rock_production
            rock1_sarawak_royalties += rock.miner_data.royalties.royalties

        rock1_sabah_list = rock1_list.filter(miner_data__quarry__state='SBH')
        rock1_sabah_production = 0
        rock1_sabah_royalties = 0
        for rock in rock1_sabah_list:
            rock1_sabah_production += rock.miner_data.productionstatistic.main_rock_production
            rock1_sabah_royalties += rock.miner_data.royalties.royalties

        rock1 = {
            'name': rock_type1,
            'perlis': {
                'production': rock1_perlis_production,
                'royalties': rock1_perlis_royalties,
            },
            'kedah': {
                'production': rock1_kedah_production,
                'royalties': rock1_kedah_royalties,
            },
            'penang': {
                'production': rock1_penang_production,
                'royalties': rock1_penang_royalties,
            },
            'perak': {
                'production': rock1_perak_production,
                'royalties': rock1_perak_royalties,
            },
            'selangor': {
                'production': rock1_selangor_production,
                'royalties': rock1_selangor_royalties,
            },
            'nsembilan': {
                'production': rock1_nsembilan_production,
                'royalties': rock1_nsembilan_royalties,
            },
            'melaka': {
                'production': rock1_melaka_production,
                'royalties': rock1_melaka_royalties,
            },
            'johor': {
                'production': rock1_johor_production,
                'royalties': rock1_johor_royalties,
            },
            'pahang': {
                'production': rock1_pahang_production,
                'royalties': rock1_pahang_royalties,
            },
            'terengganu': {
                'production': rock1_terengganu_production,
                'royalties': rock1_terengganu_royalties,
            },
            'kelantan': {
                'production': rock1_kelantan_production,
                'royalties': rock1_kelantan_royalties,
            },
            'sarawak': {
                'production': rock1_sarawak_production,
                'royalties': rock1_sarawak_royalties,
            },
            'sabah': {
                'production': rock1_sabah_production,
                'royalties': rock1_sabah_royalties,
            },
        }

        total_by_state = {
            'perlis': {
                'production': sum([rock1['perlis']["production"]]),
                'royalties': sum([rock1['perlis']["royalties"]]),
            },
            'kedah': {
                'production': sum([rock1['kedah']["production"]]),
                'royalties': sum([rock1['kedah']["royalties"]]),
            },
            'penang': {
                'production': sum([rock1['penang']["production"]]),
                'royalties': sum([rock1['penang']["royalties"]]),
            },
            'perak': {
                'production': sum([rock1['perak']["production"]]),
                'royalties': sum([rock1['perak']["royalties"]]),
            },
            'selangor': {
                'production': sum([rock1['selangor']["production"]]),
                'royalties': sum([rock1['selangor']["royalties"]]),
            },
            'nsembilan': {
                'production': sum([rock1['nsembilan']["production"]]),
                'royalties': sum([rock1['nsembilan']["royalties"]]),
            },
            'melaka': {
                'production': sum([rock1['melaka']["production"]]),
                'royalties': sum([rock1['melaka']["royalties"]]),
            },
            'johor': {
                'production': sum([rock1['johor']["production"]]),
                'royalties': sum([rock1['johor']["royalties"]]),
            },
            'pahang': {
                'production': sum([rock1['pahang']["production"]]),
                'royalties': sum([rock1['pahang']["royalties"]]),
            },
            'terengganu': {
                'production': sum([rock1['terengganu']["production"]]),
                'royalties': sum([rock1['terengganu']["royalties"]]),
            },
            'kelantan': {
                'production': sum([rock1['kelantan']["production"]]),
                'royalties': sum([rock1['kelantan']["royalties"]]),
            },
            'sarawak': {
                'production': sum([rock1['sarawak']["production"]]),
                'royalties': sum([rock1['sarawak']["royalties"]]),
            },
            'sabah': {
                'production': sum([rock1['sabah']["production"]]),
                'royalties': sum([rock1['sabah']["royalties"]]),
            },
        }

        states = [
            {
                'name': 'PERLIS',
                'rock1': rock1['perlis'],
                'total_by_state': total_by_state['perlis'],
            },
            {
                'name': 'KEDAH',
                'rock1': rock1['kedah'],
                'total_by_state': total_by_state['kedah'],
            },
            {
                'name': 'PULAU PINANG',
                'rock1': rock1['penang'],
                'total_by_state': total_by_state['penang'],
            },
            {
                'name': 'PERAK',
                'rock1': rock1['perak'],
                'total_by_state': total_by_state['perak'],
            },
            {
                'name': 'SELANGOR',
                'rock1': rock1['selangor'],
                'total_by_state': total_by_state['selangor'],
            },
            {
                'name': 'NEGERI SEMBILAN',
                'rock1': rock1['nsembilan'],
                'total_by_state': total_by_state['nsembilan'],
            },
            {
                'name': 'MELAKA',
                'rock1': rock1['melaka'],
                'total_by_state': total_by_state['melaka'],
            },
            {
                'name': 'JOHOR',
                'rock1': rock1['johor'],
                'total_by_state': total_by_state['johor'],
            },
            {
                'name': 'PAHANG',
                'rock1': rock1['pahang'],
                'total_by_state': total_by_state['pahang'],
            },
            {
                'name': 'PERLIS',
                'rock1': rock1['terengganu'],
                'total_by_state': total_by_state['terengganu'],
            },
            {
                'name': 'KELANTAN',
                'rock1': rock1['kelantan'],
                'total_by_state': total_by_state['kelantan'],
            },
            {
                'name': 'SARAWAK',
                'rock1': rock1['sarawak'],
                'total_by_state': total_by_state['sarawak'],
            },
            {
                'name': 'SABAH',
                'rock1': rock1['sabah'],
                'total_by_state': total_by_state['sabah'],
            },
        ]

        rocks = {
            'rock1': {
                'name': rock_type1,
                'production': sum([state['rock1']['production'] for state in states]),
            }
        }

        total = {
            'production': sum([state['total_by_state']['production'] for state in states]),
            'royalties': sum([state['total_by_state']['royalties'] for state in states]),
        }

        if month:
            month = dict(form.fields['month'].choices)[int(month)]

        context = {
            'title': 'Laporan/Graph Kuari',
            'form': form,
            'year': year,
            'month': month,
            'rocks': rocks,
            'states': states,
            'total': total,
        }

        return render(request, 'report/hq/graph/data.html', context)

    context = {
        'form': form,
        'title': 'Laporan/Graph Kuari',
    }

    return render(request, 'report/hq/graph/form.html', context)
