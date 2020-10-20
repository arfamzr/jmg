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

        def get_rock_list(rock_list):
            rock_perlis_list = rock_list.filter(
                miner_data__quarry__state='PLS')
            rock_perlis_production = 0
            rock_perlis_royalties = 0
            for rock in rock_perlis_list:
                rock_perlis_production += rock.miner_data.productionstatistic.main_rock_production
                rock_perlis_royalties += rock.miner_data.royalties.royalties

            rock_kedah_list = rock_list.filter(miner_data__quarry__state='KDH')
            rock_kedah_production = 0
            rock_kedah_royalties = 0
            for rock in rock_kedah_list:
                rock_kedah_production += rock.miner_data.productionstatistic.main_rock_production
                rock_kedah_royalties += rock.miner_data.royalties.royalties

            rock_penang_list = rock_list.filter(
                miner_data__quarry__state='PNG')
            rock_penang_production = 0
            rock_penang_royalties = 0
            for rock in rock_penang_list:
                rock_penang_production += rock.miner_data.productionstatistic.main_rock_production
                rock_penang_royalties += rock.miner_data.royalties.royalties

            rock_perak_list = rock_list.filter(miner_data__quarry__state='PRK')
            rock_perak_production = 0
            rock_perak_royalties = 0
            for rock in rock_perak_list:
                rock_perak_production += rock.miner_data.productionstatistic.main_rock_production
                rock_perak_royalties += rock.miner_data.royalties.royalties

            rock_selangor_list = rock_list.filter(
                miner_data__quarry__state='SGR')
            rock_selangor_production = 0
            rock_selangor_royalties = 0
            for rock in rock_selangor_list:
                rock_selangor_production += rock.miner_data.productionstatistic.main_rock_production
                rock_selangor_royalties += rock.miner_data.royalties.royalties

            rock_nsembilan_list = rock_list.filter(
                miner_data__quarry__state='PLS')
            rock_nsembilan_production = 0
            rock_nsembilan_royalties = 0
            for rock in rock_nsembilan_list:
                rock_nsembilan_production += rock.miner_data.productionstatistic.main_rock_production
                rock_nsembilan_royalties += rock.miner_data.royalties.royalties

            rock_melaka_list = rock_list.filter(
                miner_data__quarry__state='MLK')
            rock_melaka_production = 0
            rock_melaka_royalties = 0
            for rock in rock_melaka_list:
                rock_melaka_production += rock.miner_data.productionstatistic.main_rock_production
                rock_melaka_royalties += rock.miner_data.royalties.royalties

            rock_johor_list = rock_list.filter(miner_data__quarry__state='JHR')
            rock_johor_production = 0
            rock_johor_royalties = 0
            for rock in rock_johor_list:
                rock_johor_production += rock.miner_data.productionstatistic.main_rock_production
                rock_johor_royalties += rock.miner_data.royalties.royalties

            rock_pahang_list = rock_list.filter(
                miner_data__quarry__state='PHG')
            rock_pahang_production = 0
            rock_pahang_royalties = 0
            for rock in rock_pahang_list:
                rock_pahang_production += rock.miner_data.productionstatistic.main_rock_production
                rock_pahang_royalties += rock.miner_data.royalties.royalties

            rock_terengganu_list = rock_list.filter(
                miner_data__quarry__state='TRG')
            rock_terengganu_production = 0
            rock_terengganu_royalties = 0
            for rock in rock_terengganu_list:
                rock_terengganu_production += rock.miner_data.productionstatistic.main_rock_production
                rock_terengganu_royalties += rock.miner_data.royalties.royalties

            rock_kelantan_list = rock_list.filter(
                miner_data__quarry__state='KTN')
            rock_kelantan_production = 0
            rock_kelantan_royalties = 0
            for rock in rock_kelantan_list:
                rock_kelantan_production += rock.miner_data.productionstatistic.main_rock_production
                rock_kelantan_royalties += rock.miner_data.royalties.royalties

            rock_sarawak_list = rock_list.filter(
                miner_data__quarry__state='SWK')
            rock_sarawak_production = 0
            rock_sarawak_royalties = 0
            for rock in rock_sarawak_list:
                rock_sarawak_production += rock.miner_data.productionstatistic.main_rock_production
                rock_sarawak_royalties += rock.miner_data.royalties.royalties

            rock_sabah_list = rock_list.filter(miner_data__quarry__state='SBH')
            rock_sabah_production = 0
            rock_sabah_royalties = 0
            for rock in rock_sabah_list:
                rock_sabah_production += rock.miner_data.productionstatistic.main_rock_production
                rock_sabah_royalties += rock.miner_data.royalties.royalties

            rock = {
                'perlis': {
                    'production': rock_perlis_production,
                    'royalties': rock_perlis_royalties,
                },
                'kedah': {
                    'production': rock_kedah_production,
                    'royalties': rock_kedah_royalties,
                },
                'penang': {
                    'production': rock_penang_production,
                    'royalties': rock_penang_royalties,
                },
                'perak': {
                    'production': rock_perak_production,
                    'royalties': rock_perak_royalties,
                },
                'selangor': {
                    'production': rock_selangor_production,
                    'royalties': rock_selangor_royalties,
                },
                'nsembilan': {
                    'production': rock_nsembilan_production,
                    'royalties': rock_nsembilan_royalties,
                },
                'melaka': {
                    'production': rock_melaka_production,
                    'royalties': rock_melaka_royalties,
                },
                'johor': {
                    'production': rock_johor_production,
                    'royalties': rock_johor_royalties,
                },
                'pahang': {
                    'production': rock_pahang_production,
                    'royalties': rock_pahang_royalties,
                },
                'terengganu': {
                    'production': rock_terengganu_production,
                    'royalties': rock_terengganu_royalties,
                },
                'kelantan': {
                    'production': rock_kelantan_production,
                    'royalties': rock_kelantan_royalties,
                },
                'sarawak': {
                    'production': rock_sarawak_production,
                    'royalties': rock_sarawak_royalties,
                },
                'sabah': {
                    'production': rock_sabah_production,
                    'royalties': rock_sabah_royalties,
                },
            }

            return rock

        rock1 = get_rock_list(rock1_list)
        rock2 = get_rock_list(rock2_list)
        rock3 = get_rock_list(rock3_list)
        rock4 = get_rock_list(rock4_list)
        rock5 = get_rock_list(rock5_list)

        total_by_state = {
            'perlis': {
                'production': sum([
                    rock1['perlis']["production"],
                    rock2['perlis']["production"],
                    rock3['perlis']["production"],
                    rock4['perlis']["production"],
                    rock5['perlis']["production"],
                ]),
                'royalties': sum([
                    rock1['perlis']["royalties"],
                    rock2['perlis']["royalties"],
                    rock3['perlis']["royalties"],
                    rock4['perlis']["royalties"],
                    rock5['perlis']["royalties"],
                ]),
            },
            'kedah': {
                'production': sum([
                    rock1['kedah']["production"],
                    rock2['kedah']["production"],
                    rock3['kedah']["production"],
                    rock4['kedah']["production"],
                    rock5['kedah']["production"],
                ]),
                'royalties': sum([
                    rock1['kedah']["royalties"],
                    rock2['kedah']["royalties"],
                    rock3['kedah']["royalties"],
                    rock4['kedah']["royalties"],
                    rock5['kedah']["royalties"],
                ]),
            },
            'penang': {
                'production': sum([
                    rock1['penang']["production"],
                    rock2['penang']["production"],
                    rock3['penang']["production"],
                    rock4['penang']["production"],
                    rock5['penang']["production"],
                ]),
                'royalties': sum([
                    rock1['penang']["royalties"],
                    rock2['penang']["royalties"],
                    rock3['penang']["royalties"],
                    rock4['penang']["royalties"],
                    rock5['penang']["royalties"],
                ]),
            },
            'perak': {
                'production': sum([
                    rock1['perak']["production"],
                    rock2['perak']["production"],
                    rock3['perak']["production"],
                    rock4['perak']["production"],
                    rock5['perak']["production"],
                ]),
                'royalties': sum([
                    rock1['perak']["royalties"],
                    rock2['perak']["royalties"],
                    rock3['perak']["royalties"],
                    rock4['perak']["royalties"],
                    rock5['perak']["royalties"],
                ]),
            },
            'selangor': {
                'production': sum([
                    rock1['selangor']["production"],
                    rock2['selangor']["production"],
                    rock3['selangor']["production"],
                    rock4['selangor']["production"],
                    rock5['selangor']["production"],
                ]),
                'royalties': sum([
                    rock1['selangor']["royalties"],
                    rock2['selangor']["royalties"],
                    rock3['selangor']["royalties"],
                    rock4['selangor']["royalties"],
                    rock5['selangor']["royalties"],
                ]),
            },
            'nsembilan': {
                'production': sum([
                    rock1['nsembilan']["production"],
                    rock2['nsembilan']["production"],
                    rock3['nsembilan']["production"],
                    rock4['nsembilan']["production"],
                    rock5['nsembilan']["production"],
                ]),
                'royalties': sum([
                    rock1['nsembilan']["royalties"],
                    rock2['nsembilan']["royalties"],
                    rock3['nsembilan']["royalties"],
                    rock4['nsembilan']["royalties"],
                    rock5['nsembilan']["royalties"],
                ]),
            },
            'melaka': {
                'production': sum([
                    rock1['melaka']["production"],
                    rock2['melaka']["production"],
                    rock3['melaka']["production"],
                    rock4['melaka']["production"],
                    rock5['melaka']["production"],
                ]),
                'royalties': sum([
                    rock1['melaka']["royalties"],
                    rock2['melaka']["royalties"],
                    rock3['melaka']["royalties"],
                    rock4['melaka']["royalties"],
                    rock5['melaka']["royalties"],
                ]),
            },
            'johor': {
                'production': sum([
                    rock1['johor']["production"],
                    rock2['johor']["production"],
                    rock3['johor']["production"],
                    rock4['johor']["production"],
                    rock5['johor']["production"],
                ]),
                'royalties': sum([
                    rock1['johor']["royalties"],
                    rock2['johor']["royalties"],
                    rock3['johor']["royalties"],
                    rock4['johor']["royalties"],
                    rock5['johor']["royalties"],
                ]),
            },
            'pahang': {
                'production': sum([
                    rock1['pahang']["production"],
                    rock2['pahang']["production"],
                    rock3['pahang']["production"],
                    rock4['pahang']["production"],
                    rock5['pahang']["production"],
                ]),
                'royalties': sum([
                    rock1['pahang']["royalties"],
                    rock2['pahang']["royalties"],
                    rock3['pahang']["royalties"],
                    rock4['pahang']["royalties"],
                    rock5['pahang']["royalties"],
                ]),
            },
            'terengganu': {
                'production': sum([
                    rock1['terengganu']["production"],
                    rock2['terengganu']["production"],
                    rock3['terengganu']["production"],
                    rock4['terengganu']["production"],
                    rock5['terengganu']["production"],
                ]),
                'royalties': sum([
                    rock1['terengganu']["royalties"],
                    rock2['terengganu']["royalties"],
                    rock3['terengganu']["royalties"],
                    rock4['terengganu']["royalties"],
                    rock5['terengganu']["royalties"],
                ]),
            },
            'kelantan': {
                'production': sum([
                    rock1['kelantan']["production"],
                    rock2['kelantan']["production"],
                    rock3['kelantan']["production"],
                    rock4['kelantan']["production"],
                    rock5['kelantan']["production"],
                ]),
                'royalties': sum([
                    rock1['kelantan']["royalties"],
                    rock2['kelantan']["royalties"],
                    rock3['kelantan']["royalties"],
                    rock4['kelantan']["royalties"],
                    rock5['kelantan']["royalties"],
                ]),
            },
            'sarawak': {
                'production': sum([
                    rock1['sarawak']["production"],
                    rock2['sarawak']["production"],
                    rock3['sarawak']["production"],
                    rock4['sarawak']["production"],
                    rock5['sarawak']["production"],
                ]),
                'royalties': sum([
                    rock1['sarawak']["royalties"],
                    rock2['sarawak']["royalties"],
                    rock3['sarawak']["royalties"],
                    rock4['sarawak']["royalties"],
                    rock5['sarawak']["royalties"],
                ]),
            },
            'sabah': {
                'production': sum([
                    rock1['sabah']["production"],
                    rock2['sabah']["production"],
                    rock3['sabah']["production"],
                    rock4['sabah']["production"],
                    rock5['sabah']["production"],
                ]),
                'royalties': sum([
                    rock1['sabah']["royalties"],
                    rock2['sabah']["royalties"],
                    rock3['sabah']["royalties"],
                    rock4['sabah']["royalties"],
                    rock5['sabah']["royalties"],
                ]),
            },
        }

        states = [
            {
                'name': 'PERLIS',
                'rock1': rock1['perlis'],
                'rock2': rock2['perlis'],
                'rock3': rock3['perlis'],
                'rock4': rock4['perlis'],
                'rock5': rock5['perlis'],
                'total_by_state': total_by_state['perlis'],
            },
            {
                'name': 'KEDAH',
                'rock1': rock1['kedah'],
                'rock2': rock2['kedah'],
                'rock3': rock3['kedah'],
                'rock4': rock4['kedah'],
                'rock5': rock5['kedah'],
                'total_by_state': total_by_state['kedah'],
            },
            {
                'name': 'PULAU PINANG',
                'rock1': rock1['penang'],
                'rock2': rock2['penang'],
                'rock3': rock3['penang'],
                'rock4': rock4['penang'],
                'rock5': rock5['penang'],
                'total_by_state': total_by_state['penang'],
            },
            {
                'name': 'PERAK',
                'rock1': rock1['perak'],
                'rock2': rock2['perak'],
                'rock3': rock3['perak'],
                'rock4': rock4['perak'],
                'rock5': rock5['perak'],
                'total_by_state': total_by_state['perak'],
            },
            {
                'name': 'SELANGOR',
                'rock1': rock1['selangor'],
                'rock2': rock2['selangor'],
                'rock3': rock3['selangor'],
                'rock4': rock4['selangor'],
                'rock5': rock5['selangor'],
                'total_by_state': total_by_state['selangor'],
            },
            {
                'name': 'NEGERI SEMBILAN',
                'rock1': rock1['nsembilan'],
                'rock2': rock2['nsembilan'],
                'rock3': rock3['nsembilan'],
                'rock4': rock4['nsembilan'],
                'rock5': rock5['nsembilan'],
                'total_by_state': total_by_state['nsembilan'],
            },
            {
                'name': 'MELAKA',
                'rock1': rock1['melaka'],
                'rock2': rock2['melaka'],
                'rock3': rock3['melaka'],
                'rock4': rock4['melaka'],
                'rock5': rock5['melaka'],
                'total_by_state': total_by_state['melaka'],
            },
            {
                'name': 'JOHOR',
                'rock1': rock1['johor'],
                'rock2': rock2['johor'],
                'rock3': rock3['johor'],
                'rock4': rock4['johor'],
                'rock5': rock5['johor'],
                'total_by_state': total_by_state['johor'],
            },
            {
                'name': 'PAHANG',
                'rock1': rock1['pahang'],
                'rock2': rock2['pahang'],
                'rock3': rock3['pahang'],
                'rock4': rock4['pahang'],
                'rock5': rock5['pahang'],
                'total_by_state': total_by_state['pahang'],
            },
            {
                'name': 'PERLIS',
                'rock1': rock1['terengganu'],
                'rock2': rock2['terengganu'],
                'rock3': rock3['terengganu'],
                'rock4': rock4['terengganu'],
                'rock5': rock5['terengganu'],
                'total_by_state': total_by_state['terengganu'],
            },
            {
                'name': 'KELANTAN',
                'rock1': rock1['kelantan'],
                'rock2': rock2['kelantan'],
                'rock3': rock3['kelantan'],
                'rock4': rock4['kelantan'],
                'rock5': rock5['kelantan'],
                'total_by_state': total_by_state['kelantan'],
            },
            {
                'name': 'SARAWAK',
                'rock1': rock1['sarawak'],
                'rock2': rock2['sarawak'],
                'rock3': rock3['sarawak'],
                'rock4': rock4['sarawak'],
                'rock5': rock5['sarawak'],
                'total_by_state': total_by_state['sarawak'],
            },
            {
                'name': 'SABAH',
                'rock1': rock1['sabah'],
                'rock2': rock2['sabah'],
                'rock3': rock3['sabah'],
                'rock4': rock4['sabah'],
                'rock5': rock5['sabah'],
                'total_by_state': total_by_state['sabah'],
            },
        ]

        rocks = {
            'rock1': {
                'name': rock_type1,
                'production': sum([state['rock1']['production'] for state in states]),
            },
            'rock2': {
                'name': rock_type2,
                'production': sum([state['rock2']['production'] for state in states]),
            },
            'rock3': {
                'name': rock_type3,
                'production': sum([state['rock3']['production'] for state in states]),
            },
            'rock4': {
                'name': rock_type4,
                'production': sum([state['rock4']['production'] for state in states]),
            },
            'rock5': {
                'name': rock_type5,
                'production': sum([state['rock5']['production'] for state in states]),
            },
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
