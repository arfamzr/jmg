from django.shortcuts import render, redirect, HttpResponse, Http404

import xlwt
from datetime import datetime

from quarry.models import QuarryDataApproval
from mine.models import MineDataApproval

from ..forms.state_admin import ReportForm


def quarry_report_input(request):
    form = ReportForm()

    context = {
        'form': form,
        'title': 'Laporan Kuari',
    }

    return render(request, 'report/state_admin/quarry/form.html', context)


def mine_report_input(request):
    form = ReportForm()

    context = {
        'form': form,
        'title': 'Laporan Lombong',
    }

    return render(request, 'report/state_admin/mine/form.html', context)


def quarry_report(request):
    form = ReportForm(request.GET)
    if form.is_valid():
        year = form.cleaned_data['year']
        month = form.cleaned_data['month']
        rock_type = form.cleaned_data['rock_type']

        datas = QuarryDataApproval.objects.filter(
            admin_approved=True,
            miner_data__year=year, miner_data__month=month,
            miner_data__quarry__main_rock_type=rock_type,
            miner_data__quarry__state=request.user.profile.state)

        if not datas:
            raise Http404

        wb = xlwt.Workbook(encoding='utf-8')
        ws_statistic = wb.add_sheet('Perangkaan Pengeluaran')
        ws_submission = wb.add_sheet('Penyerahan Jualan')
        ws_worker_operator = wb.add_sheet('Jumlah Pekerja (Operator)')
        ws_worker_contractor = wb.add_sheet('Jumlah Pekerja (Kontraktor)')
        ws_combustion_machinery = wb.add_sheet('Jentera Bakar Dalam')
        ws_electric_machinery = wb.add_sheet('Jentera Elektrik')
        ws_explosive = wb.add_sheet('Penggunaan Bahan Letupan')
        ws_energy = wb.add_sheet('Bahan Tenaga')

        font_bold = xlwt.XFStyle()
        font_bold.font.bold = True

        font_style = xlwt.XFStyle()

        # Perangkaan Pengeluaran HEADER
        statistic_row = 0

        statistic_headers = ['Bil', 'Syarikat (Mukim)', 'Daerah', 'Stok Awal Bulan',
                             'Pengeluaran', 'Jumlah', 'Jualan', 'Stok Akhir Bulan', 'Royalti (RM)']

        for col_num in range(len(statistic_headers)):
            ws_statistic.write(statistic_row, col_num,
                               statistic_headers[col_num], font_bold)

        # Penyerahan Jualan HEADER
        submission_row = 0
        submission_headers = ['Crusher Run', 'Quarry Dust', 'Quarry Waste', '1/8"', '3/8"',
                              '5/8"', '3/4"', '1"', '1 1/2"', '2"', '3" x 5"', '6" x 9"', 'Block', 'Jumlah']

        for col_num in range(len(submission_headers)):
            ws_submission.write(submission_row, col_num,
                                submission_headers[col_num], font_bold)

        # Jumlah Pekerja (Operator) HEADER
        worker_operator_row = 0

        ws_worker_operator.write_merge(0, 0, 0, 9, 'Tempatan', font_bold)
        ws_worker_operator.write_merge(0, 0, 10, 19, 'Asing', font_bold)

        worker_operator_row += 1

        ws_worker_operator.write_merge(1, 1, 0, 1, 'Pengurusan', font_bold)
        ws_worker_operator.write_merge(1, 1, 10, 11, 'Pengurusan', font_bold)
        ws_worker_operator.write_merge(1, 1, 2, 3, 'Profesional', font_bold)
        ws_worker_operator.write_merge(1, 1, 12, 13, 'Profesional', font_bold)
        ws_worker_operator.write_merge(1, 1, 4, 5, 'Teknikal', font_bold)
        ws_worker_operator.write_merge(1, 1, 14, 15, 'Teknikal', font_bold)
        ws_worker_operator.write_merge(1, 1, 6, 7, 'Kerani', font_bold)
        ws_worker_operator.write_merge(1, 1, 16, 17, 'Kerani', font_bold)
        ws_worker_operator.write_merge(1, 1, 8, 9, 'Buruh', font_bold)
        ws_worker_operator.write_merge(1, 1, 18, 19, 'Buruh', font_bold)

        worker_operator_row += 1

        ws_worker_operator.write(2, 0, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 1, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 2, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 3, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 4, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 5, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 6, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 7, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 8, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 9, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 10, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 11, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 12, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 13, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 14, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 15, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 16, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 17, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 18, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 19, 'Perempuan', font_bold)

        ws_worker_operator.write_merge(0, 2, 20, 20, 'Jumlah', font_bold)
        ws_worker_operator.write_merge(
            0, 2, 21, 21, 'Jumlah Gaji (RM)', font_bold)
        ws_worker_operator.write_merge(
            0, 2, 22, 22, 'Jumlah jam manusia', font_bold)

        # Jumlah Pekerja (Kontraktor) HEADER
        worker_contractor_row = 0

        ws_worker_contractor.write_merge(0, 0, 0, 9, 'Tempatan', font_bold)
        ws_worker_contractor.write_merge(0, 0, 10, 19, 'Asing', font_bold)

        worker_contractor_row += 1

        ws_worker_contractor.write_merge(1, 1, 0, 1, 'Pengurusan', font_bold)
        ws_worker_contractor.write_merge(1, 1, 10, 11, 'Pengurusan', font_bold)
        ws_worker_contractor.write_merge(1, 1, 2, 3, 'Profesional', font_bold)
        ws_worker_contractor.write_merge(
            1, 1, 12, 13, 'Profesional', font_bold)
        ws_worker_contractor.write_merge(1, 1, 4, 5, 'Teknikal', font_bold)
        ws_worker_contractor.write_merge(1, 1, 14, 15, 'Teknikal', font_bold)
        ws_worker_contractor.write_merge(1, 1, 6, 7, 'Kerani', font_bold)
        ws_worker_contractor.write_merge(1, 1, 16, 17, 'Kerani', font_bold)
        ws_worker_contractor.write_merge(1, 1, 8, 9, 'Buruh', font_bold)
        ws_worker_contractor.write_merge(1, 1, 18, 19, 'Buruh', font_bold)

        worker_contractor_row += 1

        ws_worker_contractor.write(2, 0, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 1, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 2, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 3, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 4, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 5, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 6, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 7, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 8, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 9, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 10, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 11, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 12, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 13, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 14, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 15, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 16, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 17, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 18, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 19, 'Perempuan', font_bold)

        ws_worker_contractor.write_merge(0, 2, 20, 20, 'Jumlah', font_bold)
        ws_worker_contractor.write_merge(
            0, 2, 21, 21, 'Jumlah Gaji (RM)', font_bold)
        ws_worker_contractor.write_merge(
            0, 2, 22, 22, 'Jumlah jam manusia', font_bold)

        # Jentera Bakar Dalam HEADER
        combustion_machinery_row = 0

        ws_combustion_machinery.write_merge(0, 0, 0, 1, 'Lori', font_bold)
        ws_combustion_machinery.write_merge(0, 0, 2, 3, 'Jengkorek', font_bold)
        ws_combustion_machinery.write_merge(
            0, 0, 4, 5, 'Jentera Angkut Beroda', font_bold)
        ws_combustion_machinery.write_merge(0, 0, 6, 7, 'Jentolak', font_bold)
        ws_combustion_machinery.write_merge(0, 0, 8, 9, 'Pam Air', font_bold)
        ws_combustion_machinery.write_merge(
            0, 0, 10, 11, 'Pemampat Udara', font_bold)
        ws_combustion_machinery.write_merge(
            0, 0, 12, 13, 'Pemecah Hidraulik', font_bold)
        ws_combustion_machinery.write_merge(
            0, 0, 14, 15, 'Gerudi Hidraulik', font_bold)
        ws_combustion_machinery.write_merge(
            0, 0, 16, 17, 'Penghancur', font_bold)
        ws_combustion_machinery.write_merge(
            0, 0, 18, 19, 'Penyuduk', font_bold)
        ws_combustion_machinery.write_merge(0, 0, 20, 21, 'Traktor', font_bold)
        ws_combustion_machinery.write_merge(0, 0, 22, 23, 'Lain', font_bold)
        ws_combustion_machinery.write_merge(0, 0, 24, 25, 'Jumlah', font_bold)

        combustion_machinery_row += 1

        ws_combustion_machinery.write(1, 0, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 1, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 2, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 3, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 4, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 5, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 6, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 7, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 8, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 9, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 10, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 11, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 12, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 13, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 14, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 15, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 16, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 17, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 18, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 19, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 20, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 21, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 22, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 23, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 24, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 25, 'Kw', font_bold)

        # Jentera Elektrik HEADER
        electric_machinery_row = 0

        ws_electric_machinery.write_merge(0, 0, 0, 1, 'Pam Air', font_bold)
        ws_electric_machinery.write_merge(
            0, 0, 2, 3, 'Pemampat Udara', font_bold)
        ws_electric_machinery.write_merge(0, 0, 4, 5, 'Penghancur', font_bold)
        ws_electric_machinery.write_merge(0, 0, 6, 7, 'Lain', font_bold)
        ws_electric_machinery.write_merge(0, 0, 8, 9, 'Jumlah', font_bold)
        ws_electric_machinery.write_merge(
            0, 0, 10, 11, 'Jumlah besar', font_bold)

        electric_machinery_row += 1

        ws_electric_machinery.write(1, 0, 'Bil', font_bold)
        ws_electric_machinery.write(1, 1, 'Kw', font_bold)
        ws_electric_machinery.write(1, 2, 'Bil', font_bold)
        ws_electric_machinery.write(1, 3, 'Kw', font_bold)
        ws_electric_machinery.write(1, 4, 'Bil', font_bold)
        ws_electric_machinery.write(1, 5, 'Kw', font_bold)
        ws_electric_machinery.write(1, 6, 'Bil', font_bold)
        ws_electric_machinery.write(1, 7, 'Kw', font_bold)
        ws_electric_machinery.write(1, 8, 'Bil', font_bold)
        ws_electric_machinery.write(1, 9, 'Kw', font_bold)
        ws_electric_machinery.write(1, 10, 'Bil', font_bold)
        ws_electric_machinery.write(1, 11, 'Kw', font_bold)

        # Penggunaan Bahan Letupan HEADER
        explosive_row = 0

        ws_explosive.write_merge(0, 0, 0, 2, 'Bahan Letupan (kg)', font_bold)
        ws_explosive.write_merge(0, 0, 3, 5, 'Detonator (biji)', font_bold)
        ws_explosive.write_merge(0, 1, 6, 6, 'Fius Keselamatan (m)', font_bold)
        ws_explosive.write_merge(0, 1, 7, 7, 'Kord Peledak (m)', font_bold)
        ws_explosive.write_merge(0, 1, 8, 8, 'ANFO (kg)', font_bold)
        ws_explosive.write_merge(0, 1, 9, 9, 'Bulk Emulsion (kg)', font_bold)
        ws_explosive.write_merge(0, 1, 10, 10, 'Relay (biji)', font_bold)

        explosive_row += 1

        ws_explosive.write(1, 0, 'Bes Emulsi', font_bold)
        ws_explosive.write(1, 1, 'Bes Nitro Gliserin', font_bold)
        ws_explosive.write(1, 2, 'Lain-lain', font_bold)
        ws_explosive.write(1, 3, 'Biasa', font_bold)
        ws_explosive.write(1, 4, 'Elektrik', font_bold)
        ws_explosive.write(1, 5, 'Bukan Elektrik', font_bold)

        # Bahan Tenaga HEADER
        energy_row = 0

        ws_energy.write(0, 0, 'Diesel (LITER)', font_bold)
        ws_energy.write(0, 1, 'Elektrik (KwH)', font_bold)
        ws_energy.write(0, 2, 'Jam Operasi Sehari', font_bold)
        ws_energy.write(0, 3, 'Bil. Hari Operasi', font_bold)

        # set data for all
        statistic_datas = []
        submission_datas = []
        worker_operator_datas = []
        worker_contractor_datas = []
        combustion_machinery_datas = []
        electric_machinery_datas = []
        explosive_datas = []
        energy_datas = []

        for data in datas:
            quarry = data.miner_data.quarry
            company = data.requestor.employee.company
            statistic = data.miner_data.productionstatistic
            royalties = data.miner_data.royalties
            submission = data.miner_data.salessubmission
            local_operator = data.miner_data.localoperator
            foreign_operator = data.miner_data.foreignoperator
            local_contractor = data.miner_data.localcontractor
            foreign_contractor = data.miner_data.foreigncontractor
            combustion_machinery = data.miner_data.internalcombustionmachinery
            electric_machinery = data.miner_data.electricmachinery
            explosive = data.miner_data.daily_explosives.first()
            energy = data.miner_data.energysupply
            record = data.miner_data.operatingrecord

            statistic_datas.append([
                f'{company.name} ({quarry.mukim})',
                quarry.district,
                statistic.initial_main_rock_stock,
                statistic.main_rock_production,
                statistic.total_main_rock,
                statistic.main_rock_submission,
                statistic.final_main_rock_stock,
                royalties.royalties,
            ])

            submission_datas.append([
                submission.crusher_amount,
                submission.dust_amount,
                submission.waste_amount,
                submission.inch_1_8_amount,
                submission.inch_3_8_amount,
                submission.inch_5_8_amount,
                submission.inch_3_4_amount,
                submission.inch_1_amount,
                submission.inch_1_1_2_amount,
                submission.inch_2_amount,
                submission.inch_3x5_amount,
                submission.inch_6x9_amount,
                submission.block_amount,
            ])

            worker_operator_datas.append([
                local_operator.male_manager,
                local_operator.female_manager,
                local_operator.male_professional,
                local_operator.female_professional,
                local_operator.male_technical,
                local_operator.female_technical,
                local_operator.male_clerk,
                local_operator.female_clerk,
                local_operator.male_labor,
                local_operator.female_labor,
                foreign_operator.male_manager,
                foreign_operator.female_manager,
                foreign_operator.male_professional,
                foreign_operator.female_professional,
                foreign_operator.male_technical,
                foreign_operator.female_technical,
                foreign_operator.male_clerk,
                foreign_operator.female_clerk,
                foreign_operator.male_labor,
                foreign_operator.female_labor,
                (local_operator.total_male+local_operator.total_female +
                 foreign_operator.total_male+foreign_operator.total_female),
                (local_operator.total_male_salary+local_operator.total_female_salary +
                 foreign_operator.total_male_salary+foreign_operator.total_female_salary),
                (local_operator.male_man_hour+local_operator.female_man_hour +
                 foreign_operator.male_man_hour+foreign_operator.female_man_hour),
            ])

            worker_contractor_datas.append([
                local_contractor.male_manager,
                local_contractor.female_manager,
                local_contractor.male_professional,
                local_contractor.female_professional,
                local_contractor.male_technical,
                local_contractor.female_technical,
                local_contractor.male_clerk,
                local_contractor.female_clerk,
                local_contractor.male_labor,
                local_contractor.female_labor,
                foreign_contractor.male_manager,
                foreign_contractor.female_manager,
                foreign_contractor.male_professional,
                foreign_contractor.female_professional,
                foreign_contractor.male_technical,
                foreign_contractor.female_technical,
                foreign_contractor.male_clerk,
                foreign_contractor.female_clerk,
                foreign_contractor.male_labor,
                foreign_contractor.female_labor,
                (local_contractor.total_male+local_contractor.total_female +
                 foreign_contractor.total_male+foreign_contractor.total_female),
                (local_contractor.total_male_salary+local_contractor.total_female_salary +
                 foreign_contractor.total_male_salary+foreign_contractor.total_female_salary),
                (local_contractor.male_man_hour+local_contractor.female_man_hour +
                 foreign_contractor.male_man_hour+foreign_contractor.female_man_hour),
            ])

            combustion_machinery_datas.append([
                combustion_machinery.number_lorry,
                combustion_machinery.lorry_power,
                combustion_machinery.number_excavator,
                combustion_machinery.excavator_power,
                combustion_machinery.number_wheel_loader,
                combustion_machinery.wheel_loader_power,
                combustion_machinery.number_bulldozer,
                combustion_machinery.bulldozer_power,
                combustion_machinery.number_water_pump,
                combustion_machinery.water_pump_power,
                combustion_machinery.number_air_compressor,
                combustion_machinery.air_compressor_power,
                combustion_machinery.number_hydraulic_breaker,
                combustion_machinery.hydraulic_breaker_power,
                combustion_machinery.number_hydraulic_drill,
                combustion_machinery.hydraulic_drill_power,
                combustion_machinery.number_crusher,
                combustion_machinery.crusher_power,
                combustion_machinery.number_shovel,
                combustion_machinery.shovel_power,
                combustion_machinery.number_tracktor,
                combustion_machinery.tracktor_power,
                combustion_machinery.number_other,
                combustion_machinery.other_power,
                combustion_machinery.total_number,
                combustion_machinery.total_power,
            ])

            electric_machinery_datas.append([
                electric_machinery.number_water_pump,
                electric_machinery.water_pump_power,
                electric_machinery.number_air_compressor,
                electric_machinery.air_compressor_power,
                electric_machinery.number_crusher,
                electric_machinery.crusher_power,
                electric_machinery.number_other,
                electric_machinery.other_power,
                electric_machinery.total_number,
                electric_machinery.total_power,
                (combustion_machinery.total_number+electric_machinery.total_number),
                (combustion_machinery.total_power+electric_machinery.total_power),
            ])

            explosive_datas.append([
                explosive.emulsion_explosive,
                explosive.ng_explosive,
                explosive.other_explosive,
                explosive.detonator,
                explosive.electric_detonator,
                explosive.non_electric_detonator,
                explosive.safety_fuse,
                explosive.detonating_cord,
                explosive.anfo,
                explosive.bulk_emulsion,
                explosive.relay_tld,
            ])

            energy_datas.append([
                energy.total_diesel,
                energy.total_electric,
                record.operating_hours,
                record.operating_days,
            ])

        # Data Perangkaan Pengeluaran

        for index, row in enumerate(statistic_datas):
            statistic_row += 1
            ws_statistic.write(statistic_row, 0, index+1)

            for col_num in range(len(row)):
                ws_statistic.write(statistic_row, col_num+1,
                                   row[col_num], font_style)

        statistic_row += 1

        statistic_col_alpha = list(map(chr, range(ord('D'), ord('I')+1)))

        ws_statistic.write_merge(
            statistic_row, statistic_row, 0, 2, f'JUMLAH ({rock_type})', font_bold)

        for index, alpha in enumerate(statistic_col_alpha):
            ws_statistic.write(statistic_row, index+3, xlwt.Formula(
                f'SUM({alpha}2:{alpha}{statistic_row})'), font_bold)

        # Data Penyerahan Jualan

        for row in submission_datas:
            submission_row += 1

            for col_num in range(len(row)):
                ws_submission.write(submission_row, col_num,
                                    row[col_num], font_style)

            ws_submission.write(submission_row, len(row), xlwt.Formula(
                f'SUM(A{submission_row+1}:M{submission_row+1})'), font_bold)

        submission_row += 1

        submission_col_alpha = list(map(chr, range(ord('A'), ord('N')+1)))

        for index, alpha in enumerate(submission_col_alpha):
            ws_submission.write(submission_row, index, xlwt.Formula(
                f'SUM({alpha}2:{alpha}{submission_row})'), font_bold)

        # Data Jumlah Pekerja (Operator)

        for row in worker_operator_datas:
            worker_operator_row += 1

            for col_num in range(len(row)):
                ws_worker_operator.write(worker_operator_row, col_num,
                                         row[col_num], font_style)

        worker_operator_row += 1

        worker_operator_col_alpha = list(map(chr, range(ord('A'), ord('W')+1)))

        for index, alpha in enumerate(worker_operator_col_alpha):
            ws_worker_operator.write(worker_operator_row, index, xlwt.Formula(
                f'SUM({alpha}4:{alpha}{worker_operator_row})'), font_bold)

        # Data Jumlah Pekerja (Kontractor)

        for row in worker_contractor_datas:
            worker_contractor_row += 1

            for col_num in range(len(row)):
                ws_worker_contractor.write(worker_contractor_row, col_num,
                                           row[col_num], font_style)

        worker_contractor_row += 1

        worker_contractor_col_alpha = list(
            map(chr, range(ord('A'), ord('W')+1)))

        for index, alpha in enumerate(worker_contractor_col_alpha):
            ws_worker_contractor.write(worker_contractor_row, index, xlwt.Formula(
                f'SUM({alpha}4:{alpha}{worker_contractor_row})'), font_bold)

        # Data Jentera Bakar Dalam

        for row in combustion_machinery_datas:
            combustion_machinery_row += 1

            for col_num in range(len(row)):
                ws_combustion_machinery.write(combustion_machinery_row, col_num,
                                              row[col_num], font_style)

        combustion_machinery_row += 1

        combustion_machinery_col_alpha = list(
            map(chr, range(ord('A'), ord('Z')+1)))

        for index, alpha in enumerate(combustion_machinery_col_alpha):
            ws_combustion_machinery.write(combustion_machinery_row, index, xlwt.Formula(
                f'SUM({alpha}3:{alpha}{combustion_machinery_row})'), font_bold)

        # Data Jentera Elektrik

        for row in electric_machinery_datas:
            electric_machinery_row += 1

            for col_num in range(len(row)):
                ws_electric_machinery.write(electric_machinery_row, col_num,
                                            row[col_num], font_style)

        electric_machinery_row += 1

        electric_machinery_col_alpha = list(
            map(chr, range(ord('A'), ord('L')+1)))

        for index, alpha in enumerate(electric_machinery_col_alpha):
            ws_electric_machinery.write(electric_machinery_row, index, xlwt.Formula(
                f'SUM({alpha}3:{alpha}{electric_machinery_row})'), font_bold)

        # Data Penggunaan Bahan Letupan

        for row in explosive_datas:
            explosive_row += 1

            for col_num in range(len(row)):
                ws_explosive.write(explosive_row, col_num,
                                   row[col_num], font_style)

        explosive_row += 1

        explosive_col_alpha = list(map(chr, range(ord('A'), ord('K')+1)))

        for index, alpha in enumerate(explosive_col_alpha):
            ws_explosive.write(explosive_row, index, xlwt.Formula(
                f'SUM({alpha}3:{alpha}{explosive_row})'), font_bold)

        # Data Bahan Tenaga

        for row in energy_datas:
            energy_row += 1

            for col_num in range(len(row)):
                ws_energy.write(energy_row, col_num,
                                row[col_num], font_style)

        energy_row += 1

        energy_col_alpha = list(map(chr, range(ord('A'), ord('D')+1)))

        for index, alpha in enumerate(energy_col_alpha):
            ws_energy.write(energy_row, index, xlwt.Formula(
                f'SUM({alpha}3:{alpha}{energy_row})'), font_bold)

        # render response
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=ReportKuari_' + \
            rock_type + '_' + month + '_' + year + '.xls'

        # excel to response
        wb.save(response)

        return response

    else:
        return redirect('report:state_admin:quarry_input')


def mine_report(request):
    form = ReportForm(request.GET)
    if form.is_valid():
        year = form.cleaned_data['year']
        month = form.cleaned_data['month']
        rock_type = form.cleaned_data['rock_type']

        datas = MineDataApproval.objects.filter(
            admin_approved=True,
            miner_data__year=year, miner_data__month=month,
            miner_data__mine__main_rock_type=rock_type,
            miner_data__mine__state=request.user.profile.state)

        if not datas:
            raise Http404

        wb = xlwt.Workbook(encoding='utf-8')
        ws_statistic = wb.add_sheet('Perangkaan Mineral/Logam')
        ws_worker_operator = wb.add_sheet('Jumlah Pekerja (Operator)')
        ws_worker_contractor = wb.add_sheet('Jumlah Pekerja (Kontraktor)')
        ws_combustion_machinery = wb.add_sheet('Jentera Bakar Dalam')
        ws_electric_machinery = wb.add_sheet('Jentera Elektrik')
        ws_energy = wb.add_sheet('Bahan Tenaga')
        ws_record_operation = wb.add_sheet('Rekod Operasi')

        font_bold = xlwt.XFStyle()
        font_bold.font.bold = True

        font_style = xlwt.XFStyle()

        # Perangkaan Pengeluaran HEADER
        statistic_row = 0

        statistic_headers = ['Bil', 'Syarikat (Mukim)', 'Daerah', 'Stok Akhir Bulan Lalu',
                             'Pengeluaran Lombong', 'Jumlah', 'Penyerahan kepada Pembeli', 'Stok Akhir Bulan Ini', 'Gred Hitung Panjang']

        for col_num in range(len(statistic_headers)):
            ws_statistic.write(statistic_row, col_num,
                               statistic_headers[col_num], font_bold)

        # Jumlah Pekerja (Operator) HEADER
        worker_operator_row = 0

        ws_worker_operator.write_merge(0, 0, 0, 9, 'Tempatan', font_bold)
        ws_worker_operator.write_merge(0, 0, 10, 19, 'Asing', font_bold)

        worker_operator_row += 1

        ws_worker_operator.write_merge(1, 1, 0, 1, 'Pengurusan', font_bold)
        ws_worker_operator.write_merge(1, 1, 10, 11, 'Pengurusan', font_bold)
        ws_worker_operator.write_merge(1, 1, 2, 3, 'Profesional', font_bold)
        ws_worker_operator.write_merge(1, 1, 12, 13, 'Profesional', font_bold)
        ws_worker_operator.write_merge(1, 1, 4, 5, 'Teknikal', font_bold)
        ws_worker_operator.write_merge(1, 1, 14, 15, 'Teknikal', font_bold)
        ws_worker_operator.write_merge(1, 1, 6, 7, 'Kerani', font_bold)
        ws_worker_operator.write_merge(1, 1, 16, 17, 'Kerani', font_bold)
        ws_worker_operator.write_merge(1, 1, 8, 9, 'Buruh', font_bold)
        ws_worker_operator.write_merge(1, 1, 18, 19, 'Buruh', font_bold)

        worker_operator_row += 1

        ws_worker_operator.write(2, 0, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 1, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 2, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 3, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 4, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 5, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 6, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 7, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 8, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 9, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 10, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 11, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 12, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 13, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 14, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 15, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 16, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 17, 'Perempuan', font_bold)
        ws_worker_operator.write(2, 18, 'Lelaki', font_bold)
        ws_worker_operator.write(2, 19, 'Perempuan', font_bold)

        ws_worker_operator.write_merge(0, 2, 20, 20, 'Jumlah', font_bold)
        ws_worker_operator.write_merge(
            0, 2, 21, 21, 'Jumlah Gaji (RM)', font_bold)
        ws_worker_operator.write_merge(
            0, 2, 22, 22, 'Jumlah jam manusia', font_bold)

        # Jumlah Pekerja (Kontraktor) HEADER
        worker_contractor_row = 0

        ws_worker_contractor.write_merge(0, 0, 0, 9, 'Tempatan', font_bold)
        ws_worker_contractor.write_merge(0, 0, 10, 19, 'Asing', font_bold)

        worker_contractor_row += 1

        ws_worker_contractor.write_merge(1, 1, 0, 1, 'Pengurusan', font_bold)
        ws_worker_contractor.write_merge(1, 1, 10, 11, 'Pengurusan', font_bold)
        ws_worker_contractor.write_merge(1, 1, 2, 3, 'Profesional', font_bold)
        ws_worker_contractor.write_merge(
            1, 1, 12, 13, 'Profesional', font_bold)
        ws_worker_contractor.write_merge(1, 1, 4, 5, 'Teknikal', font_bold)
        ws_worker_contractor.write_merge(1, 1, 14, 15, 'Teknikal', font_bold)
        ws_worker_contractor.write_merge(1, 1, 6, 7, 'Kerani', font_bold)
        ws_worker_contractor.write_merge(1, 1, 16, 17, 'Kerani', font_bold)
        ws_worker_contractor.write_merge(1, 1, 8, 9, 'Buruh', font_bold)
        ws_worker_contractor.write_merge(1, 1, 18, 19, 'Buruh', font_bold)

        worker_contractor_row += 1

        ws_worker_contractor.write(2, 0, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 1, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 2, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 3, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 4, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 5, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 6, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 7, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 8, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 9, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 10, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 11, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 12, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 13, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 14, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 15, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 16, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 17, 'Perempuan', font_bold)
        ws_worker_contractor.write(2, 18, 'Lelaki', font_bold)
        ws_worker_contractor.write(2, 19, 'Perempuan', font_bold)

        ws_worker_contractor.write_merge(0, 2, 20, 20, 'Jumlah', font_bold)
        ws_worker_contractor.write_merge(
            0, 2, 21, 21, 'Jumlah Gaji (RM)', font_bold)
        ws_worker_contractor.write_merge(
            0, 2, 22, 22, 'Jumlah jam manusia', font_bold)

        # Jentera Bakar Dalam HEADER
        combustion_machinery_row = 0

        ws_combustion_machinery.write_merge(0, 0, 0, 1, 'Lori', font_bold)
        ws_combustion_machinery.write_merge(0, 0, 2, 3, 'Jengkorek', font_bold)
        ws_combustion_machinery.write_merge(
            0, 0, 4, 5, 'Jentera Angkut Beroda', font_bold)
        ws_combustion_machinery.write_merge(0, 0, 6, 7, 'Jentolak', font_bold)
        ws_combustion_machinery.write_merge(0, 0, 8, 9, 'Pam Air', font_bold)
        ws_combustion_machinery.write_merge(
            0, 0, 10, 11, 'Pemampat Udara', font_bold)
        ws_combustion_machinery.write_merge(
            0, 0, 12, 13, 'Pemecah Hidraulik', font_bold)
        ws_combustion_machinery.write_merge(
            0, 0, 14, 15, 'Gerudi Hidraulik', font_bold)
        ws_combustion_machinery.write_merge(
            0, 0, 16, 17, 'Penghancur', font_bold)
        ws_combustion_machinery.write_merge(
            0, 0, 18, 19, 'Penyuduk', font_bold)
        ws_combustion_machinery.write_merge(0, 0, 20, 21, 'Traktor', font_bold)
        ws_combustion_machinery.write_merge(0, 0, 22, 23, 'Lain', font_bold)
        ws_combustion_machinery.write_merge(0, 0, 24, 25, 'Jumlah', font_bold)

        combustion_machinery_row += 1

        ws_combustion_machinery.write(1, 0, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 1, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 2, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 3, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 4, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 5, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 6, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 7, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 8, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 9, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 10, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 11, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 12, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 13, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 14, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 15, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 16, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 17, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 18, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 19, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 20, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 21, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 22, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 23, 'Kw', font_bold)
        ws_combustion_machinery.write(1, 24, 'Bil', font_bold)
        ws_combustion_machinery.write(1, 25, 'Kw', font_bold)

        # Jentera Elektrik HEADER
        electric_machinery_row = 0

        ws_electric_machinery.write_merge(0, 0, 0, 1, 'Pam Air', font_bold)
        ws_electric_machinery.write_merge(
            0, 0, 2, 3, 'Pemampat Udara', font_bold)
        ws_electric_machinery.write_merge(0, 0, 4, 5, 'Penghancur', font_bold)
        ws_electric_machinery.write_merge(0, 0, 6, 7, 'Lain', font_bold)
        ws_electric_machinery.write_merge(0, 0, 8, 9, 'Jumlah', font_bold)
        ws_electric_machinery.write_merge(
            0, 0, 10, 11, 'Jumlah besar', font_bold)

        electric_machinery_row += 1

        ws_electric_machinery.write(1, 0, 'Bil', font_bold)
        ws_electric_machinery.write(1, 1, 'Kw', font_bold)
        ws_electric_machinery.write(1, 2, 'Bil', font_bold)
        ws_electric_machinery.write(1, 3, 'Kw', font_bold)
        ws_electric_machinery.write(1, 4, 'Bil', font_bold)
        ws_electric_machinery.write(1, 5, 'Kw', font_bold)
        ws_electric_machinery.write(1, 6, 'Bil', font_bold)
        ws_electric_machinery.write(1, 7, 'Kw', font_bold)
        ws_electric_machinery.write(1, 8, 'Bil', font_bold)
        ws_electric_machinery.write(1, 9, 'Kw', font_bold)
        ws_electric_machinery.write(1, 10, 'Bil', font_bold)
        ws_electric_machinery.write(1, 11, 'Kw', font_bold)

        # Bahan Tenaga HEADER
        energy_row = 0

        ws_energy.write(0, 0, 'Diesel (LITER)', font_bold)
        ws_energy.write(0, 1, 'Elektrik (KwH)', font_bold)
        ws_energy.write(0, 2, 'Jam Operasi Sehari', font_bold)
        ws_energy.write(0, 3, 'Bil. Hari Operasi', font_bold)

        # Rekod Operasi HEADER
        energy_row = 0

        ws_energy.write(0, 0, 'Dalam lombong hitung panjang, meter', font_bold)
        ws_energy.write(0, 1, 'Ukuran lombong terdalam, meter', font_bold)
        ws_energy.write(0, 2, 'Ukuran lombong tercetek, meter', font_bold)
        ws_energy.write(0, 3, 'Bahan beban dibuang, tan', font_bold)
        ws_energy.write(0, 4, 'Bahan berbijih dilombong, tan', font_bold)

        # set data for all
        statistic_datas = []
        worker_operator_datas = []
        worker_contractor_datas = []
        combustion_machinery_datas = []
        electric_machinery_datas = []
        energy_datas = []
        record_operation_datas = []

        for data in datas:
            mine = data.miner_data.mine
            company = data.requestor.employee.company
            statistic = data.miner_data.productionstatistic
            royalties = data.miner_data.royalties
            local_operator = data.miner_data.localoperator
            foreign_operator = data.miner_data.foreignoperator
            local_contractor = data.miner_data.localcontractor
            foreign_contractor = data.miner_data.foreigncontractor
            combustion_machinery = data.miner_data.internalcombustionmachinery
            electric_machinery = data.miner_data.electricmachinery
            energy = data.miner_data.energysupply
            record_operation = data.miner_data.operatingrecord

            statistic_datas.append([
                f'{company.name} ({mine.mukim})',
                mine.district,
                statistic.initial_main_rock_stock,
                statistic.main_rock_production,
                statistic.total_main_rock,
                statistic.main_rock_submission,
                statistic.final_main_rock_stock,
                royalties.royalties,
            ])

            worker_operator_datas.append([
                local_operator.male_manager,
                local_operator.female_manager,
                local_operator.male_professional,
                local_operator.female_professional,
                local_operator.male_technical,
                local_operator.female_technical,
                local_operator.male_clerk,
                local_operator.female_clerk,
                local_operator.male_labor,
                local_operator.female_labor,
                foreign_operator.male_manager,
                foreign_operator.female_manager,
                foreign_operator.male_professional,
                foreign_operator.female_professional,
                foreign_operator.male_technical,
                foreign_operator.female_technical,
                foreign_operator.male_clerk,
                foreign_operator.female_clerk,
                foreign_operator.male_labor,
                foreign_operator.female_labor,
                (local_operator.total_male+local_operator.total_female +
                    foreign_operator.total_male+foreign_operator.total_female),
                (local_operator.total_male_salary+local_operator.total_female_salary +
                    foreign_operator.total_male_salary+foreign_operator.total_female_salary),
                (local_operator.male_man_hour+local_operator.female_man_hour +
                    foreign_operator.male_man_hour+foreign_operator.female_man_hour),
            ])

            worker_contractor_datas.append([
                local_contractor.male_manager,
                local_contractor.female_manager,
                local_contractor.male_professional,
                local_contractor.female_professional,
                local_contractor.male_technical,
                local_contractor.female_technical,
                local_contractor.male_clerk,
                local_contractor.female_clerk,
                local_contractor.male_labor,
                local_contractor.female_labor,
                foreign_contractor.male_manager,
                foreign_contractor.female_manager,
                foreign_contractor.male_professional,
                foreign_contractor.female_professional,
                foreign_contractor.male_technical,
                foreign_contractor.female_technical,
                foreign_contractor.male_clerk,
                foreign_contractor.female_clerk,
                foreign_contractor.male_labor,
                foreign_contractor.female_labor,
                (local_contractor.total_male+local_contractor.total_female +
                    foreign_contractor.total_male+foreign_contractor.total_female),
                (local_contractor.total_male_salary+local_contractor.total_female_salary +
                    foreign_contractor.total_male_salary+foreign_contractor.total_female_salary),
                (local_contractor.male_man_hour+local_contractor.female_man_hour +
                    foreign_contractor.male_man_hour+foreign_contractor.female_man_hour),
            ])

            combustion_machinery_datas.append([
                combustion_machinery.number_lorry,
                combustion_machinery.lorry_power,
                combustion_machinery.number_excavator,
                combustion_machinery.excavator_power,
                combustion_machinery.number_wheel_loader,
                combustion_machinery.wheel_loader_power,
                combustion_machinery.number_bulldozer,
                combustion_machinery.bulldozer_power,
                combustion_machinery.number_water_pump,
                combustion_machinery.water_pump_power,
                combustion_machinery.number_air_compressor,
                combustion_machinery.air_compressor_power,
                combustion_machinery.number_hydraulic_breaker,
                combustion_machinery.hydraulic_breaker_power,
                combustion_machinery.number_hydraulic_drill,
                combustion_machinery.hydraulic_drill_power,
                combustion_machinery.number_crusher,
                combustion_machinery.crusher_power,
                combustion_machinery.number_shovel,
                combustion_machinery.shovel_power,
                combustion_machinery.number_tracktor,
                combustion_machinery.tracktor_power,
                combustion_machinery.number_other,
                combustion_machinery.other_power,
                combustion_machinery.total_number,
                combustion_machinery.total_power,
            ])

            electric_machinery_datas.append([
                electric_machinery.number_water_pump,
                electric_machinery.water_pump_power,
                electric_machinery.number_air_compressor,
                electric_machinery.air_compressor_power,
                electric_machinery.number_crusher,
                electric_machinery.crusher_power,
                electric_machinery.number_other,
                electric_machinery.other_power,
                electric_machinery.total_number,
                electric_machinery.total_power,
                (combustion_machinery.total_number+electric_machinery.total_number),
                (combustion_machinery.total_power+electric_machinery.total_power),
            ])

            energy_datas.append([
                energy.total_diesel,
                energy.total_electric,
                record.operating_hours,
                record.operating_days,
            ])

            record_operation_datas.append([
                record_operation.average_mine_depth,
                record_operation.total_deepest_mine,
                record_operation.shallowest_mine,
                record_operation.material_discarded,
                record_operation.ore_mined,
            ])

        # Data Perangkaan Pengeluaran

        for index, row in enumerate(statistic_datas):
            statistic_row += 1
            ws_statistic.write(statistic_row, 0, index+1)

            for col_num in range(len(row)):
                ws_statistic.write(statistic_row, col_num+1,
                                   row[col_num], font_style)

        statistic_row += 1

        statistic_col_alpha = list(map(chr, range(ord('D'), ord('I')+1)))

        ws_statistic.write_merge(
            statistic_row, statistic_row, 0, 2, f'JUMLAH ({rock_type})', font_bold)

        for index, alpha in enumerate(statistic_col_alpha):
            ws_statistic.write(statistic_row, index+3, xlwt.Formula(
                f'SUM({alpha}2:{alpha}{statistic_row})'), font_bold)

        # Data Jumlah Pekerja (Operator)

        for row in worker_operator_datas:
            worker_operator_row += 1

            for col_num in range(len(row)):
                ws_worker_operator.write(worker_operator_row, col_num,
                                         row[col_num], font_style)

        worker_operator_row += 1

        worker_operator_col_alpha = list(map(chr, range(ord('A'), ord('W')+1)))

        for index, alpha in enumerate(worker_operator_col_alpha):
            ws_worker_operator.write(worker_operator_row, index, xlwt.Formula(
                f'SUM({alpha}4:{alpha}{worker_operator_row})'), font_bold)

        # Data Jumlah Pekerja (Kontractor)

        for row in worker_contractor_datas:
            worker_contractor_row += 1

            for col_num in range(len(row)):
                ws_worker_contractor.write(worker_contractor_row, col_num,
                                           row[col_num], font_style)

        worker_contractor_row += 1

        worker_contractor_col_alpha = list(
            map(chr, range(ord('A'), ord('W')+1)))

        for index, alpha in enumerate(worker_contractor_col_alpha):
            ws_worker_contractor.write(worker_contractor_row, index, xlwt.Formula(
                f'SUM({alpha}4:{alpha}{worker_contractor_row})'), font_bold)

        # Data Jentera Bakar Dalam

        for row in combustion_machinery_datas:
            combustion_machinery_row += 1

            for col_num in range(len(row)):
                ws_combustion_machinery.write(combustion_machinery_row, col_num,
                                              row[col_num], font_style)

        combustion_machinery_row += 1

        combustion_machinery_col_alpha = list(
            map(chr, range(ord('A'), ord('Z')+1)))

        for index, alpha in enumerate(combustion_machinery_col_alpha):
            ws_combustion_machinery.write(combustion_machinery_row, index, xlwt.Formula(
                f'SUM({alpha}3:{alpha}{combustion_machinery_row})'), font_bold)

        # Data Jentera Elektrik

        for row in electric_machinery_datas:
            electric_machinery_row += 1

            for col_num in range(len(row)):
                ws_electric_machinery.write(electric_machinery_row, col_num,
                                            row[col_num], font_style)

        electric_machinery_row += 1

        electric_machinery_col_alpha = list(
            map(chr, range(ord('A'), ord('L')+1)))

        for index, alpha in enumerate(electric_machinery_col_alpha):
            ws_electric_machinery.write(electric_machinery_row, index, xlwt.Formula(
                f'SUM({alpha}3:{alpha}{electric_machinery_row})'), font_bold)

        # Data Bahan Tenaga

        for row in energy_datas:
            energy_row += 1

            for col_num in range(len(row)):
                ws_energy.write(energy_row, col_num,
                                row[col_num], font_style)

        energy_row += 1

        energy_col_alpha = list(map(chr, range(ord('A'), ord('D')+1)))

        for index, alpha in enumerate(energy_col_alpha):
            ws_energy.write(energy_row, index, xlwt.Formula(
                f'SUM({alpha}3:{alpha}{energy_row})'), font_bold)

        # Rekod Operasi Tenaga

        for row in record_operation_datas:
            record_operation_row += 1

            for col_num in range(len(row)):
                ws_record_operation.write(record_operation_row, col_num,
                                          row[col_num], font_style)

        record_operation_row += 1

        record_operation_col_alpha = list(
            map(chr, range(ord('A'), ord('E')+1)))

        for index, alpha in enumerate(record_operation_col_alpha):
            ws_record_operation.write(record_operation_row, index, xlwt.Formula(
                f'SUM({alpha}3:{alpha}{record_operation_row})'), font_bold)

        # render response
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=ReportKuari_' + \
            rock_type + '_' + month + '_' + year + '.xls'

        # excel to response
        wb.save(response)

        return response

    else:
        return redirect('report:state_admin:quarry_input')
