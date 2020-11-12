from django.http import request
from django.shortcuts import render, redirect, HttpResponse, Http404, get_list_or_404

import xlwt
from datetime import datetime
from django.shortcuts import render
from django.db.models import Sum

from quarry.models import Approval as QuarryApproval, MainProductionStatistic, SideProductionStatistic
from mine.models import Approval as MineApproval, MainStatistic, SideStatistic

from ..forms.state_admin import MineReportForm, QuarryReportForm, GraphForm
from ..forms.hq import GraphForm, MineProductionGraphForm, QuarryProductionGraphForm, MineWorkerGraphForm


# mine report (export excel)
def mine_report(request):
    if request.method == 'POST':
        form = MineReportForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            rock_type = form.cleaned_data['rock_type']

            # main_statistic_list = MainStatistic.objects.filter(
            #     data__year=year, data__month=month,
            #     mineral_type=rock_type,
            #     data__mine__state=request.user.profile.state,
            #     data__approval__in=Approval.objects.filter(admin_approved=True))

            main_statistic_list = get_list_or_404(
                MainStatistic,
                data__year=year, data__month=month,
                mineral_type=rock_type,
                data__mine__state=request.user.profile.state,
                data__id__in=[approved_data.data.id for approved_data in MineApproval.objects.filter(admin_approved=True)])

            wb = xlwt.Workbook(encoding='utf-8')
            ws_statistic = wb.add_sheet('Perangkaan Mineral')
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

            statistic_headers = ['Bil', 'Nama Lombong (Mukim)', 'Daerah', 'Jenis Mineral', 'kuantiti',
                                 'Stok Akhir Bulan Lalu', 'Pengeluaran', 'Jumlah', 'Penyerahan',
                                 'Stok Akhir Bulan Ini']

            for col_num in range(len(statistic_headers)):
                ws_statistic.write(statistic_row, col_num,
                                   statistic_headers[col_num], font_bold)

            # Jumlah Pekerja (Operator) HEADER
            worker_operator_row = 0

            ws_worker_operator.write_merge(0, 0, 0, 9, 'Tempatan', font_bold)
            ws_worker_operator.write_merge(0, 0, 10, 19, 'Asing', font_bold)

            worker_operator_row += 1

            ws_worker_operator.write_merge(1, 1, 0, 1, 'Pengurusan', font_bold)
            ws_worker_operator.write_merge(
                1, 1, 10, 11, 'Pengurusan', font_bold)
            ws_worker_operator.write_merge(
                1, 1, 2, 3, 'Profesional', font_bold)
            ws_worker_operator.write_merge(
                1, 1, 12, 13, 'Profesional', font_bold)
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

            ws_worker_contractor.write_merge(
                1, 1, 0, 1, 'Pengurusan', font_bold)
            ws_worker_contractor.write_merge(
                1, 1, 10, 11, 'Pengurusan', font_bold)
            ws_worker_contractor.write_merge(
                1, 1, 2, 3, 'Profesional', font_bold)
            ws_worker_contractor.write_merge(
                1, 1, 12, 13, 'Profesional', font_bold)
            ws_worker_contractor.write_merge(1, 1, 4, 5, 'Teknikal', font_bold)
            ws_worker_contractor.write_merge(
                1, 1, 14, 15, 'Teknikal', font_bold)
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
            ws_combustion_machinery.write_merge(
                0, 0, 2, 3, 'Jengkorek', font_bold)
            ws_combustion_machinery.write_merge(
                0, 0, 4, 5, 'Jentera Angkut Beroda', font_bold)
            ws_combustion_machinery.write_merge(
                0, 0, 6, 7, 'Jentolak', font_bold)
            ws_combustion_machinery.write_merge(
                0, 0, 8, 9, 'Pam Air', font_bold)
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
            ws_combustion_machinery.write_merge(
                0, 0, 20, 21, 'Traktor', font_bold)
            ws_combustion_machinery.write_merge(
                0, 0, 22, 23, 'Lain', font_bold)
            ws_combustion_machinery.write_merge(
                0, 0, 24, 25, 'Jumlah', font_bold)

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
            ws_electric_machinery.write_merge(
                0, 0, 4, 5, 'Penghancur', font_bold)
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
            ws_energy.write(0, 2, 'jumlah Bahan Letupan (KG)', font_bold)

            # Rekod Operasi HEADER
            record_operation_row = 0

            ws_record_operation.write(
                0, 0, 'Dalam lombong hitung panjang, meter', font_bold)
            ws_record_operation.write(
                0, 1, 'Ukuran lombong terdalam, meter', font_bold)
            ws_record_operation.write(
                0, 2, 'Ukuran lombong tercetek, meter', font_bold)
            ws_record_operation.write(
                0, 3, 'Bahan beban dibuang, tan', font_bold)
            ws_record_operation.write(
                0, 4, 'Bahan berbijih dilombong, tan', font_bold)

            # set data for all
            statistic_datas = []
            worker_operator_datas = []
            worker_contractor_datas = []
            combustion_machinery_datas = []
            electric_machinery_datas = []
            energy_datas = []
            record_operation_datas = []

            for main_statistic in main_statistic_list:
                data = main_statistic.data
                mine = data.mine
                # operator = mine.operator
                statistic = main_statistic
                # royalties = data.royalties
                local_operator = data.localoperator
                foreign_operator = data.foreignoperator
                local_contractor = data.localcontractor
                foreign_contractor = data.foreigncontractor
                combustion_machinery = data.internalcombustionmachinery
                electric_machinery = data.electricmachinery
                energy = data.energysupply
                record_operation = data.operatingrecord

                statistic_datas.append([
                    f'{mine.name} ({mine.mukim})',
                    mine.district,
                    statistic.get_mineral_type_display(),
                    statistic.minerals_quantity,
                    statistic.final_stock_last_month,
                    statistic.mine_production,
                    statistic.total_minerals,
                    statistic.submission_buyers,
                    statistic.final_stock_last_month,
                    # royalties.royalties,
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
                    (combustion_machinery.total_number +
                     electric_machinery.total_number),
                    (combustion_machinery.total_power +
                     electric_machinery.total_power),
                ])

                energy_datas.append([
                    energy.total_diesel,
                    energy.total_electric,
                    energy.total_explosive,
                ])

                record_operation_datas.append([
                    record_operation.average_mine_depth,
                    record_operation.deepest_mine,
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

            statistic_col_alpha = list(map(chr, range(ord('E'), ord('J')+1)))

            ws_statistic.write_merge(
                statistic_row, statistic_row, 0, 3, f'JUMLAH ({rock_type})', font_bold)

            for index, alpha in enumerate(statistic_col_alpha):
                ws_statistic.write(statistic_row, index+4, xlwt.Formula(
                    f'SUM({alpha}2:{alpha}{statistic_row})'), font_bold)

            # Data Jumlah Pekerja (Operator)

            for row in worker_operator_datas:
                worker_operator_row += 1

                for col_num in range(len(row)):
                    ws_worker_operator.write(worker_operator_row, col_num,
                                             row[col_num], font_style)

            worker_operator_row += 1

            worker_operator_col_alpha = list(
                map(chr, range(ord('A'), ord('W')+1)))

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

            energy_col_alpha = list(map(chr, range(ord('A'), ord('C')+1)))

            for index, alpha in enumerate(energy_col_alpha):
                ws_energy.write(energy_row, index, xlwt.Formula(
                    f'SUM({alpha}2:{alpha}{energy_row})'), font_bold)

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
                    f'SUM({alpha}2:{alpha}{record_operation_row})'), font_bold)

            # render response
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=ReportKuari_' + \
                rock_type + '_' + month + '_' + year + '.xls'

            # excel to response
            wb.save(response)

            return response

    else:
        form = MineReportForm()

    context = {
        'form': form,
        'title': 'Laporan Lombong',
    }

    return render(request, 'report/state_admin/mine/form.html', context)


# quarry report (export excel)
def quarry_report(request):
    if request.method == 'POST':
        form = QuarryReportForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            rock_type = form.cleaned_data['rock_type']

            # datas = Approval.objects.filter(
            #     admin_approved=True,
            #     miner_data__year=year, miner_data__month=month,
            #     miner_data__quarry__main_rock_type=rock_type,
            #     miner_data__quarry__state=request.user.profile.state)

            main_statistic_list = get_list_or_404(
                MainProductionStatistic,
                data__year=year, data__month=month,
                rock_type=rock_type,
                data__quarry__state=request.user.profile.state,
                data__id__in=[approved_data.data.id for approved_data in QuarryApproval.objects.filter(admin_approved=True)])

            wb = xlwt.Workbook(encoding='utf-8')
            ws_statistic = wb.add_sheet('Perangkaan Pengeluaran Batuan')
            # ws_submission = wb.add_sheet('Penyerahan Jualan')
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

            statistic_headers = ['Bil', 'Nama Kuari (Mukim)', 'Daerah', 'Jenis Batuan', 'Stok Awal Bulan',
                                 'Pengeluaran', 'Jumlah', 'Jualan', 'Stok Akhir Bulan', 'Royalti (RM)']

            for col_num in range(len(statistic_headers)):
                ws_statistic.write(statistic_row, col_num,
                                   statistic_headers[col_num], font_bold)

            # Penyerahan Jualan HEADER
            # submission_row = 0
            # submission_headers = ['Crusher Run', 'Quarry Dust', 'Quarry Waste', '1/8"', '3/8"',
            #                       '5/8"', '3/4"', '1"', '1 1/2"', '2"', '3" x 5"', '6" x 9"', 'Block', 'Jumlah']

            # for col_num in range(len(submission_headers)):
            #     ws_submission.write(submission_row, col_num,
            #                         submission_headers[col_num], font_bold)

            # Jumlah Pekerja (Operator) HEADER
            worker_operator_row = 0

            ws_worker_operator.write_merge(0, 0, 0, 9, 'Tempatan', font_bold)
            ws_worker_operator.write_merge(0, 0, 10, 19, 'Asing', font_bold)

            worker_operator_row += 1

            ws_worker_operator.write_merge(1, 1, 0, 1, 'Pengurusan', font_bold)
            ws_worker_operator.write_merge(
                1, 1, 10, 11, 'Pengurusan', font_bold)
            ws_worker_operator.write_merge(
                1, 1, 2, 3, 'Profesional', font_bold)
            ws_worker_operator.write_merge(
                1, 1, 12, 13, 'Profesional', font_bold)
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

            ws_worker_contractor.write_merge(
                1, 1, 0, 1, 'Pengurusan', font_bold)
            ws_worker_contractor.write_merge(
                1, 1, 10, 11, 'Pengurusan', font_bold)
            ws_worker_contractor.write_merge(
                1, 1, 2, 3, 'Profesional', font_bold)
            ws_worker_contractor.write_merge(
                1, 1, 12, 13, 'Profesional', font_bold)
            ws_worker_contractor.write_merge(1, 1, 4, 5, 'Teknikal', font_bold)
            ws_worker_contractor.write_merge(
                1, 1, 14, 15, 'Teknikal', font_bold)
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
            ws_combustion_machinery.write_merge(
                0, 0, 2, 3, 'Jengkorek', font_bold)
            ws_combustion_machinery.write_merge(
                0, 0, 4, 5, 'Jentera Angkut Beroda', font_bold)
            ws_combustion_machinery.write_merge(
                0, 0, 6, 7, 'Jentolak', font_bold)
            ws_combustion_machinery.write_merge(
                0, 0, 8, 9, 'Pam Air', font_bold)
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
            ws_combustion_machinery.write_merge(
                0, 0, 20, 21, 'Traktor', font_bold)
            ws_combustion_machinery.write_merge(
                0, 0, 22, 23, 'Lain', font_bold)
            ws_combustion_machinery.write_merge(
                0, 0, 24, 25, 'Jumlah', font_bold)

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
            ws_electric_machinery.write_merge(
                0, 0, 4, 5, 'Penghancur', font_bold)
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

            ws_explosive.write_merge(
                0, 0, 0, 2, 'Bahan Letupan (kg)', font_bold)
            ws_explosive.write_merge(0, 0, 3, 5, 'Detonator (biji)', font_bold)
            ws_explosive.write_merge(
                0, 1, 6, 6, 'Fius Keselamatan (m)', font_bold)
            ws_explosive.write_merge(0, 1, 7, 7, 'Kord Peledak (m)', font_bold)
            ws_explosive.write_merge(0, 1, 8, 8, 'ANFO (kg)', font_bold)
            ws_explosive.write_merge(
                0, 1, 9, 9, 'Bulk Emulsion (kg)', font_bold)
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

            for main_statistic in main_statistic_list:
                data = main_statistic.data
                quarry = data.quarry
                # operator = quarri.operator
                statistic = main_statistic
                royalties = data.royalties
                # submission = data.salessubmission
                local_operator = data.localoperator
                foreign_operator = data.foreignoperator
                local_contractor = data.localcontractor
                foreign_contractor = data.foreigncontractor
                combustion_machinery = data.internalcombustionmachinery
                electric_machinery = data.electricmachinery
                explosive = data.daily_explosives.first()
                energy = data.energysupply
                record = data.operatingrecord

                statistic_datas.append([
                    f'{quarry.name} ({quarry.mukim})',
                    quarry.district,
                    statistic.get_rock_type_display(),
                    statistic.initial_rock_stock,
                    statistic.rock_production,
                    statistic.total_rock,
                    statistic.rock_submission,
                    statistic.final_rock_stock,
                    royalties.royalties,
                ])

                # submission_datas.append([
                #     submission.crusher_amount,
                #     submission.dust_amount,
                #     submission.waste_amount,
                #     submission.inch_1_8_amount,
                #     submission.inch_3_8_amount,
                #     submission.inch_5_8_amount,
                #     submission.inch_3_4_amount,
                #     submission.inch_1_amount,
                #     submission.inch_1_1_2_amount,
                #     submission.inch_2_amount,
                #     submission.inch_3x5_amount,
                #     submission.inch_6x9_amount,
                #     submission.block_amount,
                # ])

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
                    (combustion_machinery.total_number +
                     electric_machinery.total_number),
                    (combustion_machinery.total_power +
                     electric_machinery.total_power),
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

            statistic_col_alpha = list(map(chr, range(ord('E'), ord('J')+1)))

            ws_statistic.write_merge(
                statistic_row, statistic_row, 0, 3, f'JUMLAH ({rock_type})', font_bold)

            for index, alpha in enumerate(statistic_col_alpha):
                ws_statistic.write(statistic_row, index+4, xlwt.Formula(
                    f'SUM({alpha}2:{alpha}{statistic_row})'), font_bold)

            # Data Penyerahan Jualan

            # for row in submission_datas:
            #     submission_row += 1

            #     for col_num in range(len(row)):
            #         ws_submission.write(submission_row, col_num,
            #                             row[col_num], font_style)

            #     ws_submission.write(submission_row, len(row), xlwt.Formula(
            #         f'SUM(A{submission_row+1}:M{submission_row+1})'), font_bold)

            # submission_row += 1

            # submission_col_alpha = list(map(chr, range(ord('A'), ord('N')+1)))

            # for index, alpha in enumerate(submission_col_alpha):
            #     ws_submission.write(submission_row, index, xlwt.Formula(
            #         f'SUM({alpha}2:{alpha}{submission_row})'), font_bold)

            # Data Jumlah Pekerja (Operator)

            for row in worker_operator_datas:
                worker_operator_row += 1

                for col_num in range(len(row)):
                    ws_worker_operator.write(worker_operator_row, col_num,
                                             row[col_num], font_style)

            worker_operator_row += 1

            worker_operator_col_alpha = list(
                map(chr, range(ord('A'), ord('W')+1)))

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
                    f'SUM({alpha}2:{alpha}{energy_row})'), font_bold)

            # render response
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=ReportKuari_' + \
                rock_type + '_' + month + '_' + year + '.xls'

            # excel to response
            wb.save(response)

            return response

    else:
        form = QuarryReportForm()

    context = {
        'form': form,
        'title': 'Laporan Kuari'
    }

    return render(request, 'report/state_admin/quarry/form.html', context)


def mine_production_graph(request):
    if request.GET.get('main_rock_type1'):
        form = MineProductionGraphForm(request.GET)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            month = form.cleaned_data.get('month')
            main_rock_type1 = form.cleaned_data.get('main_rock_type1')
            main_rock_type2 = form.cleaned_data.get('main_rock_type2')
            main_rock_type3 = form.cleaned_data.get('main_rock_type3')
            main_rock_type4 = form.cleaned_data.get('main_rock_type4')
            main_rock_type5 = form.cleaned_data.get('main_rock_type5')
            side_rock_type1 = form.cleaned_data.get('side_rock_type1')
            side_rock_type2 = form.cleaned_data.get('side_rock_type2')
            side_rock_type3 = form.cleaned_data.get('side_rock_type3')
            side_rock_type4 = form.cleaned_data.get('side_rock_type4')
            side_rock_type5 = form.cleaned_data.get('side_rock_type5')

            if not month:
                month = 12

            main_rock_list = MainStatistic.objects.filter(
                data__year=year, data__month=month,
                data__state=request.user.profile.state,
                data__id__in=[approved_data.data.id for approved_data in MineApproval.objects.filter(admin_approved=True)])

            side_rock_list = SideStatistic.objects.filter(
                data__year=year, data__month=month,
                data__state=request.user.profile.state,
                data__id__in=[approved_data.data.id for approved_data in MineApproval.objects.filter(admin_approved=True)])

            def get_total_rock(rock_list, rock_type):
                rocks = rock_list.filter(mineral_type=rock_type)

                rock_production = 0
                for rock in rocks:
                    rock_production += rock.mine_production

                data = {
                    'name': rock_type,
                    'production': rock_production,
                }

                return data

            main_rocks = []
            main_rocks.append(get_total_rock(main_rock_list, main_rock_type1))
            if main_rock_type2:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type2))
            if main_rock_type3:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type3))
            if main_rock_type4:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type4))
            if main_rock_type5:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type5))

            side_rocks = []
            if side_rock_type1:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type1))
            if side_rock_type2:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type2))
            if side_rock_type3:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type3))
            if side_rock_type4:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type4))
            if side_rock_type5:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type5))

            month = dict(form.fields['month'].choices)[int(month)]

            context = {
                'title': f'Laporan/Graph Pengeluaran Lombong ({month} {year})',
                'year': year,
                'month': month,
                'main_rocks': main_rocks,
                'side_rocks': side_rocks,
            }

            return render(request, 'report/state_admin/mine/graph/production/report.html', context)

    else:
        form = MineProductionGraphForm()

    context = {
        'form': form,
        'title': 'Laporan/Graph Pengeluaran Lombong',
    }

    return render(request, 'report/state_admin/mine/graph/production/form.html', context)


def mine_worker_graph(request):
    if request.GET.get('main_rock_type1'):
        form = MineProductionGraphForm(request.GET)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            month = form.cleaned_data.get('month')
            main_rock_type1 = form.cleaned_data.get('main_rock_type1')
            main_rock_type2 = form.cleaned_data.get('main_rock_type2')
            main_rock_type3 = form.cleaned_data.get('main_rock_type3')
            main_rock_type4 = form.cleaned_data.get('main_rock_type4')
            main_rock_type5 = form.cleaned_data.get('main_rock_type5')
            side_rock_type1 = form.cleaned_data.get('side_rock_type1')
            side_rock_type2 = form.cleaned_data.get('side_rock_type2')
            side_rock_type3 = form.cleaned_data.get('side_rock_type3')
            side_rock_type4 = form.cleaned_data.get('side_rock_type4')
            side_rock_type5 = form.cleaned_data.get('side_rock_type5')

            if not month:
                month = 12

            main_rock_list = MainStatistic.objects.filter(
                data__year=year, data__month=month,
                data__state=request.user.profile.state,
                data__id__in=[approved_data.data.id for approved_data in MineApproval.objects.filter(admin_approved=True)])

            side_rock_list = SideStatistic.objects.filter(
                data__year=year, data__month=month,
                data__state=request.user.profile.state,
                data__id__in=[approved_data.data.id for approved_data in MineApproval.objects.filter(admin_approved=True)])

            def get_total_rock(rock_list, rock_type):
                rocks = rock_list.filter(mineral_type=rock_type)

                rock_worker = 0
                for rock in rocks:
                    rock_worker += rock.data.localoperator.total_male
                    rock_worker += rock.data.localoperator.total_female
                    rock_worker += rock.data.foreignoperator.total_male
                    rock_worker += rock.data.foreignoperator.total_female
                    rock_worker += rock.data.localcontractor.total_male
                    rock_worker += rock.data.localcontractor.total_female
                    rock_worker += rock.data.foreigncontractor.total_male
                    rock_worker += rock.data.foreigncontractor.total_female

                data = {
                    'name': rock_type,
                    'worker': rock_worker,
                }

                return data

            main_rocks = []
            main_rocks.append(get_total_rock(main_rock_list, main_rock_type1))
            if main_rock_type2:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type2))
            if main_rock_type3:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type3))
            if main_rock_type4:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type4))
            if main_rock_type5:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type5))

            side_rocks = []
            if side_rock_type1:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type1))
            if side_rock_type2:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type2))
            if side_rock_type3:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type3))
            if side_rock_type4:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type4))
            if side_rock_type5:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type5))

            month = dict(form.fields['month'].choices)[int(month)]

            context = {
                'title': f'Laporan/Graph Pekerja Lombong ({month} {year})',
                'year': year,
                'month': month,
                'main_rocks': main_rocks,
                'side_rocks': side_rocks,
            }

            return render(request, 'report/state_admin/mine/graph/worker/report.html', context)

    else:
        form = MineProductionGraphForm()

    context = {
        'form': form,
        'title': 'Laporan/Graph Pekerja Lombong',
    }

    return render(request, 'report/state_admin/mine/graph/worker/form.html', context)


def quarry_production_graph(request):
    if request.GET.get('main_rock_type1'):
        form = QuarryProductionGraphForm(request.GET)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            month = form.cleaned_data.get('month')
            main_rock_type1 = form.cleaned_data.get('main_rock_type1')
            main_rock_type2 = form.cleaned_data.get('main_rock_type2')
            main_rock_type3 = form.cleaned_data.get('main_rock_type3')
            main_rock_type4 = form.cleaned_data.get('main_rock_type4')
            main_rock_type5 = form.cleaned_data.get('main_rock_type5')
            side_rock_type1 = form.cleaned_data.get('side_rock_type1')
            side_rock_type2 = form.cleaned_data.get('side_rock_type2')
            side_rock_type3 = form.cleaned_data.get('side_rock_type3')
            side_rock_type4 = form.cleaned_data.get('side_rock_type4')
            side_rock_type5 = form.cleaned_data.get('side_rock_type5')

            if not month:
                month = 12

            main_rock_list = MainProductionStatistic.objects.filter(
                data__year=year, data__month=month,
                data__state=request.user.profile.state,
                data__id__in=[approved_data.data.id for approved_data in MineApproval.objects.filter(admin_approved=True)])

            side_rock_list = SideProductionStatistic.objects.filter(
                data__year=year, data__month=month,
                data__state=request.user.profile.state,
                data__id__in=[approved_data.data.id for approved_data in MineApproval.objects.filter(admin_approved=True)])

            def get_total_rock(rock_list, rock_type):
                rocks = rock_list.filter(rock_type=rock_type)

                rock_production = 0
                for rock in rocks:
                    rock_production += rock.rock_production

                data = {
                    'name': rock_type,
                    'production': rock_production,
                }

                return data

            main_rocks = []
            main_rocks.append(get_total_rock(main_rock_list, main_rock_type1))
            if main_rock_type2:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type2))
            if main_rock_type3:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type3))
            if main_rock_type4:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type4))
            if main_rock_type5:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type5))

            side_rocks = []
            if side_rock_type1:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type1))
            if side_rock_type2:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type2))
            if side_rock_type3:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type3))
            if side_rock_type4:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type4))
            if side_rock_type5:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type5))

            month = dict(form.fields['month'].choices)[int(month)]

            context = {
                'title': f'Laporan/Graph Pengeluaran Kuari ({month} {year})',
                'year': year,
                'month': month,
                'main_rocks': main_rocks,
                'side_rocks': side_rocks,
            }

            return render(request, 'report/state_admin/quarry/graph/production/report.html', context)

    else:
        form = QuarryProductionGraphForm()

    context = {
        'form': form,
        'title': 'Laporan/Graph Pengeluaran Kuari',
    }

    return render(request, 'report/state_admin/quarry/graph/production/form.html', context)


def quarry_worker_graph(request):
    if request.GET.get('main_rock_type1'):
        form = QuarryProductionGraphForm(request.GET)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            month = form.cleaned_data.get('month')
            main_rock_type1 = form.cleaned_data.get('main_rock_type1')
            main_rock_type2 = form.cleaned_data.get('main_rock_type2')
            main_rock_type3 = form.cleaned_data.get('main_rock_type3')
            main_rock_type4 = form.cleaned_data.get('main_rock_type4')
            main_rock_type5 = form.cleaned_data.get('main_rock_type5')
            side_rock_type1 = form.cleaned_data.get('side_rock_type1')
            side_rock_type2 = form.cleaned_data.get('side_rock_type2')
            side_rock_type3 = form.cleaned_data.get('side_rock_type3')
            side_rock_type4 = form.cleaned_data.get('side_rock_type4')
            side_rock_type5 = form.cleaned_data.get('side_rock_type5')

            if not month:
                month = 12

            main_rock_list = MainProductionStatistic.objects.filter(
                data__year=year, data__month=month,
                data__state=request.user.profile.state,
                data__id__in=[approved_data.data.id for approved_data in MineApproval.objects.filter(admin_approved=True)])

            side_rock_list = SideProductionStatistic.objects.filter(
                data__year=year, data__month=month,
                data__state=request.user.profile.state,
                data__id__in=[approved_data.data.id for approved_data in MineApproval.objects.filter(admin_approved=True)])

            def get_total_rock(rock_list, rock_type):
                rocks = rock_list.filter(rock_type=rock_type)

                rock_worker = 0
                for rock in rocks:
                    rock_worker += rock.data.localoperator.total_male
                    rock_worker += rock.data.localoperator.total_female
                    rock_worker += rock.data.foreignoperator.total_male
                    rock_worker += rock.data.foreignoperator.total_female
                    rock_worker += rock.data.localcontractor.total_male
                    rock_worker += rock.data.localcontractor.total_female
                    rock_worker += rock.data.foreigncontractor.total_male
                    rock_worker += rock.data.foreigncontractor.total_female

                data = {
                    'name': rock_type,
                    'worker': rock_worker,
                }

                return data

            main_rocks = []
            main_rocks.append(get_total_rock(main_rock_list, main_rock_type1))
            if main_rock_type2:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type2))
            if main_rock_type3:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type3))
            if main_rock_type4:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type4))
            if main_rock_type5:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type5))

            side_rocks = []
            if side_rock_type1:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type1))
            if side_rock_type2:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type2))
            if side_rock_type3:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type3))
            if side_rock_type4:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type4))
            if side_rock_type5:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type5))

            month = dict(form.fields['month'].choices)[int(month)]

            context = {
                'title': f'Laporan/Graph Pekerja Kuari ({month} {year})',
                'year': year,
                'month': month,
                'main_rocks': main_rocks,
                'side_rocks': side_rocks,
            }

            return render(request, 'report/state_admin/quarry/graph/worker/report.html', context)

    else:
        form = QuarryProductionGraphForm()

    context = {
        'form': form,
        'title': 'Laporan/Graph Pekerja Kuari',
    }

    return render(request, 'report/state_admin/quarry/graph/worker/form.html', context)


def quarry_royalties_graph(request):
    if request.GET.get('main_rock_type1'):
        form = QuarryProductionGraphForm(request.GET)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            month = form.cleaned_data.get('month')
            main_rock_type1 = form.cleaned_data.get('main_rock_type1')
            main_rock_type2 = form.cleaned_data.get('main_rock_type2')
            main_rock_type3 = form.cleaned_data.get('main_rock_type3')
            main_rock_type4 = form.cleaned_data.get('main_rock_type4')
            main_rock_type5 = form.cleaned_data.get('main_rock_type5')
            side_rock_type1 = form.cleaned_data.get('side_rock_type1')
            side_rock_type2 = form.cleaned_data.get('side_rock_type2')
            side_rock_type3 = form.cleaned_data.get('side_rock_type3')
            side_rock_type4 = form.cleaned_data.get('side_rock_type4')
            side_rock_type5 = form.cleaned_data.get('side_rock_type5')

            if not month:
                month = 12

            main_rock_list = MainProductionStatistic.objects.filter(
                data__year=year, data__month=month,
                data__state=request.user.profile.state,
                data__id__in=[approved_data.data.id for approved_data in MineApproval.objects.filter(admin_approved=True)])

            side_rock_list = SideProductionStatistic.objects.filter(
                data__year=year, data__month=month,
                data__state=request.user.profile.state,
                data__id__in=[approved_data.data.id for approved_data in MineApproval.objects.filter(admin_approved=True)])

            def get_total_rock(rock_list, rock_type):
                rocks = rock_list.filter(rock_type=rock_type)

                rock_royalties = 0
                for rock in rocks:
                    rock_royalties += rock.data.royalties.royalties

                data = {
                    'name': rock_type,
                    'royalties': rock_royalties,
                }

                return data

            main_rocks = []
            main_rocks.append(get_total_rock(main_rock_list, main_rock_type1))
            if main_rock_type2:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type2))
            if main_rock_type3:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type3))
            if main_rock_type4:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type4))
            if main_rock_type5:
                main_rocks.append(get_total_rock(
                    main_rock_list, main_rock_type5))

            side_rocks = []
            if side_rock_type1:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type1))
            if side_rock_type2:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type2))
            if side_rock_type3:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type3))
            if side_rock_type4:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type4))
            if side_rock_type5:
                side_rocks.append(get_total_rock(
                    side_rock_list, side_rock_type5))

            month = dict(form.fields['month'].choices)[int(month)]

            context = {
                'title': f'Laporan/Graph Royalti Kuari ({month} {year})',
                'year': year,
                'month': month,
                'main_rocks': main_rocks,
                'side_rocks': side_rocks,
            }

            return render(request, 'report/state_admin/quarry/graph/royalties/report.html', context)

    else:
        form = QuarryProductionGraphForm()

    context = {
        'form': form,
        'title': 'Laporan/Graph Royalti Kuari',
    }

    return render(request, 'report/state_admin/quarry/graph/royalties/form.html', context)


# def quarry_report_input(request):
#     form = ReportForm()

#     context = {
#         'form': form,
#         'title': 'Laporan Kuari',
#     }

#     return render(request, 'report/state_admin/quarry/form.html', context)


# def mine_report(request):
#     form = ReportForm(request.GET)
#     if form.is_valid():
#         year = form.cleaned_data['year']
#         month = form.cleaned_data['month']
#         rock_type = form.cleaned_data['rock_type']

#         datas = Approval.objects.filter(
#             admin_approved=True,
#             miner_data__year=year, miner_data__month=month,
#             miner_data__mine__main_rock_type=rock_type,
#             miner_data__mine__state=request.user.profile.state)

#         if not datas:
#             raise Http404

#         wb = xlwt.Workbook(encoding='utf-8')
#         ws_statistic = wb.add_sheet('Perangkaan Mineral/Logam')
#         ws_worker_operator = wb.add_sheet('Jumlah Pekerja (Operator)')
#         ws_worker_contractor = wb.add_sheet('Jumlah Pekerja (Kontraktor)')
#         ws_combustion_machinery = wb.add_sheet('Jentera Bakar Dalam')
#         ws_electric_machinery = wb.add_sheet('Jentera Elektrik')
#         ws_energy = wb.add_sheet('Bahan Tenaga')
#         ws_record_operation = wb.add_sheet('Rekod Operasi')

#         font_bold = xlwt.XFStyle()
#         font_bold.font.bold = True

#         font_style = xlwt.XFStyle()

#         # Perangkaan Pengeluaran HEADER
#         statistic_row = 0

#         statistic_headers = ['Bil', 'Syarikat (Mukim)', 'Daerah', 'Stok Akhir Bulan Lalu',
#                              'Pengeluaran Lombong', 'Jumlah', 'Penyerahan kepada Pembeli', 'Stok Akhir Bulan Ini', 'Gred Hitung Panjang']

#         for col_num in range(len(statistic_headers)):
#             ws_statistic.write(statistic_row, col_num,
#                                statistic_headers[col_num], font_bold)

#         # Jumlah Pekerja (Operator) HEADER
#         worker_operator_row = 0

#         ws_worker_operator.write_merge(0, 0, 0, 9, 'Tempatan', font_bold)
#         ws_worker_operator.write_merge(0, 0, 10, 19, 'Asing', font_bold)

#         worker_operator_row += 1

#         ws_worker_operator.write_merge(1, 1, 0, 1, 'Pengurusan', font_bold)
#         ws_worker_operator.write_merge(1, 1, 10, 11, 'Pengurusan', font_bold)
#         ws_worker_operator.write_merge(1, 1, 2, 3, 'Profesional', font_bold)
#         ws_worker_operator.write_merge(1, 1, 12, 13, 'Profesional', font_bold)
#         ws_worker_operator.write_merge(1, 1, 4, 5, 'Teknikal', font_bold)
#         ws_worker_operator.write_merge(1, 1, 14, 15, 'Teknikal', font_bold)
#         ws_worker_operator.write_merge(1, 1, 6, 7, 'Kerani', font_bold)
#         ws_worker_operator.write_merge(1, 1, 16, 17, 'Kerani', font_bold)
#         ws_worker_operator.write_merge(1, 1, 8, 9, 'Buruh', font_bold)
#         ws_worker_operator.write_merge(1, 1, 18, 19, 'Buruh', font_bold)

#         worker_operator_row += 1

#         ws_worker_operator.write(2, 0, 'Lelaki', font_bold)
#         ws_worker_operator.write(2, 1, 'Perempuan', font_bold)
#         ws_worker_operator.write(2, 2, 'Lelaki', font_bold)
#         ws_worker_operator.write(2, 3, 'Perempuan', font_bold)
#         ws_worker_operator.write(2, 4, 'Lelaki', font_bold)
#         ws_worker_operator.write(2, 5, 'Perempuan', font_bold)
#         ws_worker_operator.write(2, 6, 'Lelaki', font_bold)
#         ws_worker_operator.write(2, 7, 'Perempuan', font_bold)
#         ws_worker_operator.write(2, 8, 'Lelaki', font_bold)
#         ws_worker_operator.write(2, 9, 'Perempuan', font_bold)
#         ws_worker_operator.write(2, 10, 'Lelaki', font_bold)
#         ws_worker_operator.write(2, 11, 'Perempuan', font_bold)
#         ws_worker_operator.write(2, 12, 'Lelaki', font_bold)
#         ws_worker_operator.write(2, 13, 'Perempuan', font_bold)
#         ws_worker_operator.write(2, 14, 'Lelaki', font_bold)
#         ws_worker_operator.write(2, 15, 'Perempuan', font_bold)
#         ws_worker_operator.write(2, 16, 'Lelaki', font_bold)
#         ws_worker_operator.write(2, 17, 'Perempuan', font_bold)
#         ws_worker_operator.write(2, 18, 'Lelaki', font_bold)
#         ws_worker_operator.write(2, 19, 'Perempuan', font_bold)

#         ws_worker_operator.write_merge(0, 2, 20, 20, 'Jumlah', font_bold)
#         ws_worker_operator.write_merge(
#             0, 2, 21, 21, 'Jumlah Gaji (RM)', font_bold)
#         ws_worker_operator.write_merge(
#             0, 2, 22, 22, 'Jumlah jam manusia', font_bold)

#         # Jumlah Pekerja (Kontraktor) HEADER
#         worker_contractor_row = 0

#         ws_worker_contractor.write_merge(0, 0, 0, 9, 'Tempatan', font_bold)
#         ws_worker_contractor.write_merge(0, 0, 10, 19, 'Asing', font_bold)

#         worker_contractor_row += 1

#         ws_worker_contractor.write_merge(1, 1, 0, 1, 'Pengurusan', font_bold)
#         ws_worker_contractor.write_merge(1, 1, 10, 11, 'Pengurusan', font_bold)
#         ws_worker_contractor.write_merge(1, 1, 2, 3, 'Profesional', font_bold)
#         ws_worker_contractor.write_merge(
#             1, 1, 12, 13, 'Profesional', font_bold)
#         ws_worker_contractor.write_merge(1, 1, 4, 5, 'Teknikal', font_bold)
#         ws_worker_contractor.write_merge(1, 1, 14, 15, 'Teknikal', font_bold)
#         ws_worker_contractor.write_merge(1, 1, 6, 7, 'Kerani', font_bold)
#         ws_worker_contractor.write_merge(1, 1, 16, 17, 'Kerani', font_bold)
#         ws_worker_contractor.write_merge(1, 1, 8, 9, 'Buruh', font_bold)
#         ws_worker_contractor.write_merge(1, 1, 18, 19, 'Buruh', font_bold)

#         worker_contractor_row += 1

#         ws_worker_contractor.write(2, 0, 'Lelaki', font_bold)
#         ws_worker_contractor.write(2, 1, 'Perempuan', font_bold)
#         ws_worker_contractor.write(2, 2, 'Lelaki', font_bold)
#         ws_worker_contractor.write(2, 3, 'Perempuan', font_bold)
#         ws_worker_contractor.write(2, 4, 'Lelaki', font_bold)
#         ws_worker_contractor.write(2, 5, 'Perempuan', font_bold)
#         ws_worker_contractor.write(2, 6, 'Lelaki', font_bold)
#         ws_worker_contractor.write(2, 7, 'Perempuan', font_bold)
#         ws_worker_contractor.write(2, 8, 'Lelaki', font_bold)
#         ws_worker_contractor.write(2, 9, 'Perempuan', font_bold)
#         ws_worker_contractor.write(2, 10, 'Lelaki', font_bold)
#         ws_worker_contractor.write(2, 11, 'Perempuan', font_bold)
#         ws_worker_contractor.write(2, 12, 'Lelaki', font_bold)
#         ws_worker_contractor.write(2, 13, 'Perempuan', font_bold)
#         ws_worker_contractor.write(2, 14, 'Lelaki', font_bold)
#         ws_worker_contractor.write(2, 15, 'Perempuan', font_bold)
#         ws_worker_contractor.write(2, 16, 'Lelaki', font_bold)
#         ws_worker_contractor.write(2, 17, 'Perempuan', font_bold)
#         ws_worker_contractor.write(2, 18, 'Lelaki', font_bold)
#         ws_worker_contractor.write(2, 19, 'Perempuan', font_bold)

#         ws_worker_contractor.write_merge(0, 2, 20, 20, 'Jumlah', font_bold)
#         ws_worker_contractor.write_merge(
#             0, 2, 21, 21, 'Jumlah Gaji (RM)', font_bold)
#         ws_worker_contractor.write_merge(
#             0, 2, 22, 22, 'Jumlah jam manusia', font_bold)

#         # Jentera Bakar Dalam HEADER
#         combustion_machinery_row = 0

#         ws_combustion_machinery.write_merge(0, 0, 0, 1, 'Lori', font_bold)
#         ws_combustion_machinery.write_merge(0, 0, 2, 3, 'Jengkorek', font_bold)
#         ws_combustion_machinery.write_merge(
#             0, 0, 4, 5, 'Jentera Angkut Beroda', font_bold)
#         ws_combustion_machinery.write_merge(0, 0, 6, 7, 'Jentolak', font_bold)
#         ws_combustion_machinery.write_merge(0, 0, 8, 9, 'Pam Air', font_bold)
#         ws_combustion_machinery.write_merge(
#             0, 0, 10, 11, 'Pemampat Udara', font_bold)
#         ws_combustion_machinery.write_merge(
#             0, 0, 12, 13, 'Pemecah Hidraulik', font_bold)
#         ws_combustion_machinery.write_merge(
#             0, 0, 14, 15, 'Gerudi Hidraulik', font_bold)
#         ws_combustion_machinery.write_merge(
#             0, 0, 16, 17, 'Penghancur', font_bold)
#         ws_combustion_machinery.write_merge(
#             0, 0, 18, 19, 'Penyuduk', font_bold)
#         ws_combustion_machinery.write_merge(0, 0, 20, 21, 'Traktor', font_bold)
#         ws_combustion_machinery.write_merge(0, 0, 22, 23, 'Lain', font_bold)
#         ws_combustion_machinery.write_merge(0, 0, 24, 25, 'Jumlah', font_bold)

#         combustion_machinery_row += 1

#         ws_combustion_machinery.write(1, 0, 'Bil', font_bold)
#         ws_combustion_machinery.write(1, 1, 'Kw', font_bold)
#         ws_combustion_machinery.write(1, 2, 'Bil', font_bold)
#         ws_combustion_machinery.write(1, 3, 'Kw', font_bold)
#         ws_combustion_machinery.write(1, 4, 'Bil', font_bold)
#         ws_combustion_machinery.write(1, 5, 'Kw', font_bold)
#         ws_combustion_machinery.write(1, 6, 'Bil', font_bold)
#         ws_combustion_machinery.write(1, 7, 'Kw', font_bold)
#         ws_combustion_machinery.write(1, 8, 'Bil', font_bold)
#         ws_combustion_machinery.write(1, 9, 'Kw', font_bold)
#         ws_combustion_machinery.write(1, 10, 'Bil', font_bold)
#         ws_combustion_machinery.write(1, 11, 'Kw', font_bold)
#         ws_combustion_machinery.write(1, 12, 'Bil', font_bold)
#         ws_combustion_machinery.write(1, 13, 'Kw', font_bold)
#         ws_combustion_machinery.write(1, 14, 'Bil', font_bold)
#         ws_combustion_machinery.write(1, 15, 'Kw', font_bold)
#         ws_combustion_machinery.write(1, 16, 'Bil', font_bold)
#         ws_combustion_machinery.write(1, 17, 'Kw', font_bold)
#         ws_combustion_machinery.write(1, 18, 'Bil', font_bold)
#         ws_combustion_machinery.write(1, 19, 'Kw', font_bold)
#         ws_combustion_machinery.write(1, 20, 'Bil', font_bold)
#         ws_combustion_machinery.write(1, 21, 'Kw', font_bold)
#         ws_combustion_machinery.write(1, 22, 'Bil', font_bold)
#         ws_combustion_machinery.write(1, 23, 'Kw', font_bold)
#         ws_combustion_machinery.write(1, 24, 'Bil', font_bold)
#         ws_combustion_machinery.write(1, 25, 'Kw', font_bold)

#         # Jentera Elektrik HEADER
#         electric_machinery_row = 0

#         ws_electric_machinery.write_merge(0, 0, 0, 1, 'Pam Air', font_bold)
#         ws_electric_machinery.write_merge(
#             0, 0, 2, 3, 'Pemampat Udara', font_bold)
#         ws_electric_machinery.write_merge(0, 0, 4, 5, 'Penghancur', font_bold)
#         ws_electric_machinery.write_merge(0, 0, 6, 7, 'Lain', font_bold)
#         ws_electric_machinery.write_merge(0, 0, 8, 9, 'Jumlah', font_bold)
#         ws_electric_machinery.write_merge(
#             0, 0, 10, 11, 'Jumlah besar', font_bold)

#         electric_machinery_row += 1

#         ws_electric_machinery.write(1, 0, 'Bil', font_bold)
#         ws_electric_machinery.write(1, 1, 'Kw', font_bold)
#         ws_electric_machinery.write(1, 2, 'Bil', font_bold)
#         ws_electric_machinery.write(1, 3, 'Kw', font_bold)
#         ws_electric_machinery.write(1, 4, 'Bil', font_bold)
#         ws_electric_machinery.write(1, 5, 'Kw', font_bold)
#         ws_electric_machinery.write(1, 6, 'Bil', font_bold)
#         ws_electric_machinery.write(1, 7, 'Kw', font_bold)
#         ws_electric_machinery.write(1, 8, 'Bil', font_bold)
#         ws_electric_machinery.write(1, 9, 'Kw', font_bold)
#         ws_electric_machinery.write(1, 10, 'Bil', font_bold)
#         ws_electric_machinery.write(1, 11, 'Kw', font_bold)

#         # Bahan Tenaga HEADER
#         energy_row = 0

#         ws_energy.write(0, 0, 'Diesel (LITER)', font_bold)
#         ws_energy.write(0, 1, 'Elektrik (KwH)', font_bold)
#         ws_energy.write(0, 2, 'Jam Operasi Sehari', font_bold)
#         ws_energy.write(0, 3, 'Bil. Hari Operasi', font_bold)

#         # Rekod Operasi HEADER
#         energy_row = 0

#         ws_energy.write(0, 0, 'Dalam lombong hitung panjang, meter', font_bold)
#         ws_energy.write(0, 1, 'Ukuran lombong terdalam, meter', font_bold)
#         ws_energy.write(0, 2, 'Ukuran lombong tercetek, meter', font_bold)
#         ws_energy.write(0, 3, 'Bahan beban dibuang, tan', font_bold)
#         ws_energy.write(0, 4, 'Bahan berbijih dilombong, tan', font_bold)

#         # set data for all
#         statistic_datas = []
#         worker_operator_datas = []
#         worker_contractor_datas = []
#         combustion_machinery_datas = []
#         electric_machinery_datas = []
#         energy_datas = []
#         record_operation_datas = []

#         for data in datas:
#             mine = data.miner_data.mine
#             company = data.requestor.employee.company
#             statistic = data.miner_data.productionstatistic
#             royalties = data.miner_data.royalties
#             local_operator = data.miner_data.localoperator
#             foreign_operator = data.miner_data.foreignoperator
#             local_contractor = data.miner_data.localcontractor
#             foreign_contractor = data.miner_data.foreigncontractor
#             combustion_machinery = data.miner_data.internalcombustionmachinery
#             electric_machinery = data.miner_data.electricmachinery
#             energy = data.miner_data.energysupply
#             record_operation = data.miner_data.operatingrecord

#             statistic_datas.append([
#                 f'{company.name} ({mine.mukim})',
#                 mine.district,
#                 statistic.initial_main_rock_stock,
#                 statistic.main_rock_production,
#                 statistic.total_main_rock,
#                 statistic.main_rock_submission,
#                 statistic.final_main_rock_stock,
#                 royalties.royalties,
#             ])

#             worker_operator_datas.append([
#                 local_operator.male_manager,
#                 local_operator.female_manager,
#                 local_operator.male_professional,
#                 local_operator.female_professional,
#                 local_operator.male_technical,
#                 local_operator.female_technical,
#                 local_operator.male_clerk,
#                 local_operator.female_clerk,
#                 local_operator.male_labor,
#                 local_operator.female_labor,
#                 foreign_operator.male_manager,
#                 foreign_operator.female_manager,
#                 foreign_operator.male_professional,
#                 foreign_operator.female_professional,
#                 foreign_operator.male_technical,
#                 foreign_operator.female_technical,
#                 foreign_operator.male_clerk,
#                 foreign_operator.female_clerk,
#                 foreign_operator.male_labor,
#                 foreign_operator.female_labor,
#                 (local_operator.total_male+local_operator.total_female +
#                     foreign_operator.total_male+foreign_operator.total_female),
#                 (local_operator.total_male_salary+local_operator.total_female_salary +
#                     foreign_operator.total_male_salary+foreign_operator.total_female_salary),
#                 (local_operator.male_man_hour+local_operator.female_man_hour +
#                     foreign_operator.male_man_hour+foreign_operator.female_man_hour),
#             ])

#             worker_contractor_datas.append([
#                 local_contractor.male_manager,
#                 local_contractor.female_manager,
#                 local_contractor.male_professional,
#                 local_contractor.female_professional,
#                 local_contractor.male_technical,
#                 local_contractor.female_technical,
#                 local_contractor.male_clerk,
#                 local_contractor.female_clerk,
#                 local_contractor.male_labor,
#                 local_contractor.female_labor,
#                 foreign_contractor.male_manager,
#                 foreign_contractor.female_manager,
#                 foreign_contractor.male_professional,
#                 foreign_contractor.female_professional,
#                 foreign_contractor.male_technical,
#                 foreign_contractor.female_technical,
#                 foreign_contractor.male_clerk,
#                 foreign_contractor.female_clerk,
#                 foreign_contractor.male_labor,
#                 foreign_contractor.female_labor,
#                 (local_contractor.total_male+local_contractor.total_female +
#                     foreign_contractor.total_male+foreign_contractor.total_female),
#                 (local_contractor.total_male_salary+local_contractor.total_female_salary +
#                     foreign_contractor.total_male_salary+foreign_contractor.total_female_salary),
#                 (local_contractor.male_man_hour+local_contractor.female_man_hour +
#                     foreign_contractor.male_man_hour+foreign_contractor.female_man_hour),
#             ])

#             combustion_machinery_datas.append([
#                 combustion_machinery.number_lorry,
#                 combustion_machinery.lorry_power,
#                 combustion_machinery.number_excavator,
#                 combustion_machinery.excavator_power,
#                 combustion_machinery.number_wheel_loader,
#                 combustion_machinery.wheel_loader_power,
#                 combustion_machinery.number_bulldozer,
#                 combustion_machinery.bulldozer_power,
#                 combustion_machinery.number_water_pump,
#                 combustion_machinery.water_pump_power,
#                 combustion_machinery.number_air_compressor,
#                 combustion_machinery.air_compressor_power,
#                 combustion_machinery.number_hydraulic_breaker,
#                 combustion_machinery.hydraulic_breaker_power,
#                 combustion_machinery.number_hydraulic_drill,
#                 combustion_machinery.hydraulic_drill_power,
#                 combustion_machinery.number_crusher,
#                 combustion_machinery.crusher_power,
#                 combustion_machinery.number_shovel,
#                 combustion_machinery.shovel_power,
#                 combustion_machinery.number_tracktor,
#                 combustion_machinery.tracktor_power,
#                 combustion_machinery.number_other,
#                 combustion_machinery.other_power,
#                 combustion_machinery.total_number,
#                 combustion_machinery.total_power,
#             ])

#             electric_machinery_datas.append([
#                 electric_machinery.number_water_pump,
#                 electric_machinery.water_pump_power,
#                 electric_machinery.number_air_compressor,
#                 electric_machinery.air_compressor_power,
#                 electric_machinery.number_crusher,
#                 electric_machinery.crusher_power,
#                 electric_machinery.number_other,
#                 electric_machinery.other_power,
#                 electric_machinery.total_number,
#                 electric_machinery.total_power,
#                 (combustion_machinery.total_number+electric_machinery.total_number),
#                 (combustion_machinery.total_power+electric_machinery.total_power),
#             ])

#             energy_datas.append([
#                 energy.total_diesel,
#                 energy.total_electric,
#                 record.operating_hours,
#                 record.operating_days,
#             ])

#             record_operation_datas.append([
#                 record_operation.average_mine_depth,
#                 record_operation.total_deepest_mine,
#                 record_operation.shallowest_mine,
#                 record_operation.material_discarded,
#                 record_operation.ore_mined,
#             ])

#         # Data Perangkaan Pengeluaran

#         for index, row in enumerate(statistic_datas):
#             statistic_row += 1
#             ws_statistic.write(statistic_row, 0, index+1)

#             for col_num in range(len(row)):
#                 ws_statistic.write(statistic_row, col_num+1,
#                                    row[col_num], font_style)

#         statistic_row += 1

#         statistic_col_alpha = list(map(chr, range(ord('D'), ord('I')+1)))

#         ws_statistic.write_merge(
#             statistic_row, statistic_row, 0, 2, f'JUMLAH ({rock_type})', font_bold)

#         for index, alpha in enumerate(statistic_col_alpha):
#             ws_statistic.write(statistic_row, index+3, xlwt.Formula(
#                 f'SUM({alpha}2:{alpha}{statistic_row})'), font_bold)

#         # Data Jumlah Pekerja (Operator)

#         for row in worker_operator_datas:
#             worker_operator_row += 1

#             for col_num in range(len(row)):
#                 ws_worker_operator.write(worker_operator_row, col_num,
#                                          row[col_num], font_style)

#         worker_operator_row += 1

#         worker_operator_col_alpha = list(map(chr, range(ord('A'), ord('W')+1)))

#         for index, alpha in enumerate(worker_operator_col_alpha):
#             ws_worker_operator.write(worker_operator_row, index, xlwt.Formula(
#                 f'SUM({alpha}4:{alpha}{worker_operator_row})'), font_bold)

#         # Data Jumlah Pekerja (Kontractor)

#         for row in worker_contractor_datas:
#             worker_contractor_row += 1

#             for col_num in range(len(row)):
#                 ws_worker_contractor.write(worker_contractor_row, col_num,
#                                            row[col_num], font_style)

#         worker_contractor_row += 1

#         worker_contractor_col_alpha = list(
#             map(chr, range(ord('A'), ord('W')+1)))

#         for index, alpha in enumerate(worker_contractor_col_alpha):
#             ws_worker_contractor.write(worker_contractor_row, index, xlwt.Formula(
#                 f'SUM({alpha}4:{alpha}{worker_contractor_row})'), font_bold)

#         # Data Jentera Bakar Dalam

#         for row in combustion_machinery_datas:
#             combustion_machinery_row += 1

#             for col_num in range(len(row)):
#                 ws_combustion_machinery.write(combustion_machinery_row, col_num,
#                                               row[col_num], font_style)

#         combustion_machinery_row += 1

#         combustion_machinery_col_alpha = list(
#             map(chr, range(ord('A'), ord('Z')+1)))

#         for index, alpha in enumerate(combustion_machinery_col_alpha):
#             ws_combustion_machinery.write(combustion_machinery_row, index, xlwt.Formula(
#                 f'SUM({alpha}3:{alpha}{combustion_machinery_row})'), font_bold)

#         # Data Jentera Elektrik

#         for row in electric_machinery_datas:
#             electric_machinery_row += 1

#             for col_num in range(len(row)):
#                 ws_electric_machinery.write(electric_machinery_row, col_num,
#                                             row[col_num], font_style)

#         electric_machinery_row += 1

#         electric_machinery_col_alpha = list(
#             map(chr, range(ord('A'), ord('L')+1)))

#         for index, alpha in enumerate(electric_machinery_col_alpha):
#             ws_electric_machinery.write(electric_machinery_row, index, xlwt.Formula(
#                 f'SUM({alpha}3:{alpha}{electric_machinery_row})'), font_bold)

#         # Data Bahan Tenaga

#         for row in energy_datas:
#             energy_row += 1

#             for col_num in range(len(row)):
#                 ws_energy.write(energy_row, col_num,
#                                 row[col_num], font_style)

#         energy_row += 1

#         energy_col_alpha = list(map(chr, range(ord('A'), ord('D')+1)))

#         for index, alpha in enumerate(energy_col_alpha):
#             ws_energy.write(energy_row, index, xlwt.Formula(
#                 f'SUM({alpha}3:{alpha}{energy_row})'), font_bold)

#         # Rekod Operasi Tenaga

#         for row in record_operation_datas:
#             record_operation_row += 1

#             for col_num in range(len(row)):
#                 ws_record_operation.write(record_operation_row, col_num,
#                                           row[col_num], font_style)

#         record_operation_row += 1

#         record_operation_col_alpha = list(
#             map(chr, range(ord('A'), ord('E')+1)))

#         for index, alpha in enumerate(record_operation_col_alpha):
#             ws_record_operation.write(record_operation_row, index, xlwt.Formula(
#                 f'SUM({alpha}3:{alpha}{record_operation_row})'), font_bold)

#         # render response
#         response = HttpResponse(content_type='application/ms-excel')
#         response['Content-Disposition'] = 'attachment; filename=ReportKuari_' + \
#             rock_type + '_' + month + '_' + year + '.xls'

#         # excel to response
#         wb.save(response)

#         return response

#     else:
#         return redirect('report:state_admin:quarry_input')


# def quarry_graph(request):
#     form = GraphForm(request.GET)
#     if form.is_valid():
#         year = form.cleaned_data.get('year')
#         rock_type1 = form.cleaned_data.get('rock_type1')
#         rock_type2 = form.cleaned_data.get('rock_type2')
#         rock_type3 = form.cleaned_data.get('rock_type3')
#         rock_type4 = form.cleaned_data.get('rock_type4')
#         rock_type5 = form.cleaned_data.get('rock_type5')

#         rock_list = QuarryDataApproval.objects.filter(miner_data__year=year)

#         rock1_list = rock_list.filter(
#             miner_data__quarry__main_rock_type=rock_type1)
#         rock2_list = rock_list.filter(
#             miner_data__quarry__main_rock_type=rock_type2)
#         rock3_list = rock_list.filter(
#             miner_data__quarry__main_rock_type=rock_type3)
#         rock4_list = rock_list.filter(
#             miner_data__quarry__main_rock_type=rock_type4)
#         rock5_list = rock_list.filter(
#             miner_data__quarry__main_rock_type=rock_type5)

#         def get_rock_list(rock_list):
#             rock_jan_list = rock_list.filter(
#                 miner_data__month=1)
#             rock_jan_production = 0
#             rock_jan_royalties = 0
#             for rock in rock_jan_list:
#                 rock_jan_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_jan_royalties += rock.miner_data.royalties.royalties

#             rock_feb_list = rock_list.filter(
#                 miner_data__month=2)
#             rock_feb_production = 0
#             rock_feb_royalties = 0
#             for rock in rock_feb_list:
#                 rock_feb_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_feb_royalties += rock.miner_data.royalties.royalties

#             rock_mac_list = rock_list.filter(
#                 miner_data__month=3)
#             rock_mac_production = 0
#             rock_mac_royalties = 0
#             for rock in rock_mac_list:
#                 rock_mac_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_mac_royalties += rock.miner_data.royalties.royalties

#             rock_apr_list = rock_list.filter(
#                 miner_data__month=4)
#             rock_apr_production = 0
#             rock_apr_royalties = 0
#             for rock in rock_apr_list:
#                 rock_apr_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_apr_royalties += rock.miner_data.royalties.royalties

#             rock_mei_list = rock_list.filter(
#                 miner_data__month=5)
#             rock_mei_production = 0
#             rock_mei_royalties = 0
#             for rock in rock_mei_list:
#                 rock_mei_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_mei_royalties += rock.miner_data.royalties.royalties

#             rock_jun_list = rock_list.filter(
#                 miner_data__month=6)
#             rock_jun_production = 0
#             rock_jun_royalties = 0
#             for rock in rock_jun_list:
#                 rock_jun_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_jun_royalties += rock.miner_data.royalties.royalties

#             rock_jul_list = rock_list.filter(
#                 miner_data__month=7)
#             rock_jul_production = 0
#             rock_jul_royalties = 0
#             for rock in rock_jul_list:
#                 rock_jul_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_jul_royalties += rock.miner_data.royalties.royalties

#             rock_ogos_list = rock_list.filter(
#                 miner_data__month=8)
#             rock_ogos_production = 0
#             rock_ogos_royalties = 0
#             for rock in rock_ogos_list:
#                 rock_ogos_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_ogos_royalties += rock.miner_data.royalties.royalties

#             rock_sep_list = rock_list.filter(
#                 miner_data__month=9)
#             rock_sep_production = 0
#             rock_sep_royalties = 0
#             for rock in rock_sep_list:
#                 rock_sep_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_sep_royalties += rock.miner_data.royalties.royalties

#             rock_okt_list = rock_list.filter(
#                 miner_data__month=10)
#             rock_okt_production = 0
#             rock_okt_royalties = 0
#             for rock in rock_okt_list:
#                 rock_okt_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_okt_royalties += rock.miner_data.royalties.royalties

#             rock_nov_list = rock_list.filter(
#                 miner_data__month=11)
#             rock_nov_production = 0
#             rock_nov_royalties = 0
#             for rock in rock_nov_list:
#                 rock_nov_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_nov_royalties += rock.miner_data.royalties.royalties

#             rock_dis_list = rock_list.filter(
#                 miner_data__month=12)
#             rock_dis_production = 0
#             rock_dis_royalties = 0
#             for rock in rock_dis_list:
#                 rock_dis_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_dis_royalties += rock.miner_data.royalties.royalties


#             rock = {
#                 'jan': {
#                     'production': rock_jan_production,
#                     'royalties': rock_jan_royalties,
#                 },
#                 'feb': {
#                     'production': rock_feb_production,
#                     'royalties': rock_feb_royalties,
#                 },
#                 'mac': {
#                     'production': rock_mac_production,
#                     'royalties': rock_mac_royalties,
#                 },
#                 'apr': {
#                     'production': rock_apr_production,
#                     'royalties': rock_apr_royalties,
#                 },
#                 'mei': {
#                     'production': rock_mei_production,
#                     'royalties': rock_mei_royalties,
#                 },
#                 'jun': {
#                     'production': rock_jun_production,
#                     'royalties': rock_jun_royalties,
#                 },
#                 'jul': {
#                     'production': rock_jul_production,
#                     'royalties': rock_jul_royalties,
#                 },
#                 'ogos': {
#                     'production': rock_ogos_production,
#                     'royalties': rock_ogos_royalties,
#                 },
#                 'sep': {
#                     'production': rock_sep_production,
#                     'royalties': rock_sep_royalties,
#                 },
#                 'okt': {
#                     'production': rock_okt_production,
#                     'royalties': rock_okt_royalties,
#                 },
#                 'nov': {
#                     'production': rock_nov_production,
#                     'royalties': rock_nov_royalties,
#                 },
#                 'dis': {
#                     'production': rock_dis_production,
#                     'royalties': rock_dis_royalties,
#                 },
#             }

#             return rock

#         rock1 = get_rock_list(rock1_list)
#         rock2 = get_rock_list(rock2_list)
#         rock3 = get_rock_list(rock3_list)
#         rock4 = get_rock_list(rock4_list)
#         rock5 = get_rock_list(rock5_list)

#         total_by_month = {
#             'jan': {
#                 'production': sum([
#                     rock1['jan']["production"],
#                     rock2['jan']["production"],
#                     rock3['jan']["production"],
#                     rock4['jan']["production"],
#                     rock5['jan']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['jan']["royalties"],
#                     rock2['jan']["royalties"],
#                     rock3['jan']["royalties"],
#                     rock4['jan']["royalties"],
#                     rock5['jan']["royalties"],
#                 ]),
#             },
#             'feb': {
#                 'production': sum([
#                     rock1['feb']["production"],
#                     rock2['feb']["production"],
#                     rock3['feb']["production"],
#                     rock4['feb']["production"],
#                     rock5['feb']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['feb']["royalties"],
#                     rock2['feb']["royalties"],
#                     rock3['feb']["royalties"],
#                     rock4['feb']["royalties"],
#                     rock5['feb']["royalties"],
#                 ]),
#             },
#             'mac': {
#                 'production': sum([
#                     rock1['mac']["production"],
#                     rock2['mac']["production"],
#                     rock3['mac']["production"],
#                     rock4['mac']["production"],
#                     rock5['mac']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['mac']["royalties"],
#                     rock2['mac']["royalties"],
#                     rock3['mac']["royalties"],
#                     rock4['mac']["royalties"],
#                     rock5['mac']["royalties"],
#                 ]),
#             },
#             'apr': {
#                 'production': sum([
#                     rock1['apr']["production"],
#                     rock2['apr']["production"],
#                     rock3['apr']["production"],
#                     rock4['apr']["production"],
#                     rock5['apr']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['apr']["royalties"],
#                     rock2['apr']["royalties"],
#                     rock3['apr']["royalties"],
#                     rock4['apr']["royalties"],
#                     rock5['apr']["royalties"],
#                 ]),
#             },
#             'mei': {
#                 'production': sum([
#                     rock1['mei']["production"],
#                     rock2['mei']["production"],
#                     rock3['mei']["production"],
#                     rock4['mei']["production"],
#                     rock5['mei']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['mei']["royalties"],
#                     rock2['mei']["royalties"],
#                     rock3['mei']["royalties"],
#                     rock4['mei']["royalties"],
#                     rock5['mei']["royalties"],
#                 ]),
#             },
#             'jun': {
#                 'production': sum([
#                     rock1['jun']["production"],
#                     rock2['jun']["production"],
#                     rock3['jun']["production"],
#                     rock4['jun']["production"],
#                     rock5['jun']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['jun']["royalties"],
#                     rock2['jun']["royalties"],
#                     rock3['jun']["royalties"],
#                     rock4['jun']["royalties"],
#                     rock5['jun']["royalties"],
#                 ]),
#             },
#             'jul': {
#                 'production': sum([
#                     rock1['jul']["production"],
#                     rock2['jul']["production"],
#                     rock3['jul']["production"],
#                     rock4['jul']["production"],
#                     rock5['jul']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['jul']["royalties"],
#                     rock2['jul']["royalties"],
#                     rock3['jul']["royalties"],
#                     rock4['jul']["royalties"],
#                     rock5['jul']["royalties"],
#                 ]),
#             },
#             'ogos': {
#                 'production': sum([
#                     rock1['ogos']["production"],
#                     rock2['ogos']["production"],
#                     rock3['ogos']["production"],
#                     rock4['ogos']["production"],
#                     rock5['ogos']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['ogos']["royalties"],
#                     rock2['ogos']["royalties"],
#                     rock3['ogos']["royalties"],
#                     rock4['ogos']["royalties"],
#                     rock5['ogos']["royalties"],
#                 ]),
#             },
#             'sep': {
#                 'production': sum([
#                     rock1['sep']["production"],
#                     rock2['sep']["production"],
#                     rock3['sep']["production"],
#                     rock4['sep']["production"],
#                     rock5['sep']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['sep']["royalties"],
#                     rock2['sep']["royalties"],
#                     rock3['sep']["royalties"],
#                     rock4['sep']["royalties"],
#                     rock5['sep']["royalties"],
#                 ]),
#             },
#             'okt': {
#                 'production': sum([
#                     rock1['okt']["production"],
#                     rock2['okt']["production"],
#                     rock3['okt']["production"],
#                     rock4['okt']["production"],
#                     rock5['okt']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['okt']["royalties"],
#                     rock2['okt']["royalties"],
#                     rock3['okt']["royalties"],
#                     rock4['okt']["royalties"],
#                     rock5['okt']["royalties"],
#                 ]),
#             },
#             'nov': {
#                 'production': sum([
#                     rock1['nov']["production"],
#                     rock2['nov']["production"],
#                     rock3['nov']["production"],
#                     rock4['nov']["production"],
#                     rock5['nov']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['nov']["royalties"],
#                     rock2['nov']["royalties"],
#                     rock3['nov']["royalties"],
#                     rock4['nov']["royalties"],
#                     rock5['nov']["royalties"],
#                 ]),
#             },
#             'dis': {
#                 'production': sum([
#                     rock1['dis']["production"],
#                     rock2['dis']["production"],
#                     rock3['dis']["production"],
#                     rock4['dis']["production"],
#                     rock5['dis']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['dis']["royalties"],
#                     rock2['dis']["royalties"],
#                     rock3['dis']["royalties"],
#                     rock4['dis']["royalties"],
#                     rock5['dis']["royalties"],
#                 ]),
#             },
#         }

#         months = [
#             {
#                 'name': 'JANUARI',
#                 'rock1': rock1['jan'],
#                 'rock2': rock2['jan'],
#                 'rock3': rock3['jan'],
#                 'rock4': rock4['jan'],
#                 'rock5': rock5['jan'],
#                 'total_by_month': total_by_month['jan'],
#             },
#             {
#                 'name': 'FEBRUARI',
#                 'rock1': rock1['feb'],
#                 'rock2': rock2['feb'],
#                 'rock3': rock3['feb'],
#                 'rock4': rock4['feb'],
#                 'rock5': rock5['feb'],
#                 'total_by_month': total_by_month['feb'],
#             },
#             {
#                 'name': 'MAC',
#                 'rock1': rock1['mac'],
#                 'rock2': rock2['mac'],
#                 'rock3': rock3['mac'],
#                 'rock4': rock4['mac'],
#                 'rock5': rock5['mac'],
#                 'total_by_month': total_by_month['mac'],
#             },
#             {
#                 'name': 'APRIL',
#                 'rock1': rock1['apr'],
#                 'rock2': rock2['apr'],
#                 'rock3': rock3['apr'],
#                 'rock4': rock4['apr'],
#                 'rock5': rock5['apr'],
#                 'total_by_month': total_by_month['apr'],
#             },
#             {
#                 'name': 'MEI',
#                 'rock1': rock1['mei'],
#                 'rock2': rock2['mei'],
#                 'rock3': rock3['mei'],
#                 'rock4': rock4['mei'],
#                 'rock5': rock5['mei'],
#                 'total_by_month': total_by_month['mei'],
#             },
#             {
#                 'name': 'JUN',
#                 'rock1': rock1['jun'],
#                 'rock2': rock2['jun'],
#                 'rock3': rock3['jun'],
#                 'rock4': rock4['jun'],
#                 'rock5': rock5['jun'],
#                 'total_by_month': total_by_month['jun'],
#             },
#             {
#                 'name': 'JULAI',
#                 'rock1': rock1['jul'],
#                 'rock2': rock2['jul'],
#                 'rock3': rock3['jul'],
#                 'rock4': rock4['jul'],
#                 'rock5': rock5['jul'],
#                 'total_by_month': total_by_month['jul'],
#             },
#             {
#                 'name': 'OGOS',
#                 'rock1': rock1['ogos'],
#                 'rock2': rock2['ogos'],
#                 'rock3': rock3['ogos'],
#                 'rock4': rock4['ogos'],
#                 'rock5': rock5['ogos'],
#                 'total_by_month': total_by_month['ogos'],
#             },
#             {
#                 'name': 'SEPTEMBER',
#                 'rock1': rock1['sep'],
#                 'rock2': rock2['sep'],
#                 'rock3': rock3['sep'],
#                 'rock4': rock4['sep'],
#                 'rock5': rock5['sep'],
#                 'total_by_month': total_by_month['sep'],
#             },
#             {
#                 'name': 'OKTOBER',
#                 'rock1': rock1['okt'],
#                 'rock2': rock2['okt'],
#                 'rock3': rock3['okt'],
#                 'rock4': rock4['okt'],
#                 'rock5': rock5['okt'],
#                 'total_by_month': total_by_month['okt'],
#             },
#             {
#                 'name': 'NOVEMBER',
#                 'rock1': rock1['nov'],
#                 'rock2': rock2['nov'],
#                 'rock3': rock3['nov'],
#                 'rock4': rock4['nov'],
#                 'rock5': rock5['nov'],
#                 'total_by_month': total_by_month['nov'],
#             },
#             {
#                 'name': 'DISEMBER',
#                 'rock1': rock1['dis'],
#                 'rock2': rock2['dis'],
#                 'rock3': rock3['dis'],
#                 'rock4': rock4['dis'],
#                 'rock5': rock5['dis'],
#                 'total_by_month': total_by_month['dis'],
#             },
#         ]

#         rocks = {
#             'rock1': {
#                 'name': rock_type1,
#                 'production': sum([month['rock1']['production'] for month in months]),
#             },
#             'rock2': {
#                 'name': rock_type2,
#                 'production': sum([month['rock2']['production'] for month in months]),
#             },
#             'rock3': {
#                 'name': rock_type3,
#                 'production': sum([month['rock3']['production'] for month in months]),
#             },
#             'rock4': {
#                 'name': rock_type4,
#                 'production': sum([month['rock4']['production'] for month in months]),
#             },
#             'rock5': {
#                 'name': rock_type5,
#                 'production': sum([month['rock5']['production'] for month in months]),
#             },
#         }

#         total = {
#             'production': sum([month['total_by_month']['production'] for month in months]),
#             'royalties': sum([month['total_by_month']['royalties'] for month in months]),
#         }

#         context = {
#             'title': 'Laporan/Graph Kuari',
#             'form': form,
#             'year': year,
#             'rocks': rocks,
#             'months': months,
#             'total': total,
#         }

#         return render(request, 'report/state_admin/graph/quarry/data.html', context)

#     context = {
#         'form': form,
#         'title': 'Laporan/Graph Kuari',
#     }

#     return render(request, 'report/state_admin/graph/quarry/form.html', context)

# def mine_graph(request):
#     form = GraphForm(request.GET)
#     if form.is_valid():
#         year = form.cleaned_data.get('year')
#         month = form.cleaned_data.get('month')
#         rock_type1 = form.cleaned_data.get('rock_type1')
#         rock_type2 = form.cleaned_data.get('rock_type2')
#         rock_type3 = form.cleaned_data.get('rock_type3')
#         rock_type4 = form.cleaned_data.get('rock_type4')
#         rock_type5 = form.cleaned_data.get('rock_type5')

#         rock_list = MineDataApproval.objects.filter(miner_data__year=year)
#         if month:
#             rock_list.filter(miner_data__month=month)

#         rock1_list = rock_list.filter(
#             miner_data__mine__main_rock_type=rock_type1)
#         rock2_list = rock_list.filter(
#             miner_data__mine__main_rock_type=rock_type2)
#         rock3_list = rock_list.filter(
#             miner_data__mine__main_rock_type=rock_type3)
#         rock4_list = rock_list.filter(
#             miner_data__mine__main_rock_type=rock_type4)
#         rock5_list = rock_list.filter(
#             miner_data__mine__main_rock_type=rock_type5)

#         def get_rock_list(rock_list):
#             rock_perlis_list = rock_list.filter(
#                 miner_data__mine__state='PLS')
#             rock_perlis_production = 0
#             rock_perlis_royalties = 0
#             for rock in rock_perlis_list:
#                 rock_perlis_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_perlis_royalties += rock.miner_data.royalties.royalties

#             rock_kedah_list = rock_list.filter(miner_data__mine__state='KDH')
#             rock_kedah_production = 0
#             rock_kedah_royalties = 0
#             for rock in rock_kedah_list:
#                 rock_kedah_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_kedah_royalties += rock.miner_data.royalties.royalties

#             rock_penang_list = rock_list.filter(
#                 miner_data__mine__state='PNG')
#             rock_penang_production = 0
#             rock_penang_royalties = 0
#             for rock in rock_penang_list:
#                 rock_penang_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_penang_royalties += rock.miner_data.royalties.royalties

#             rock_perak_list = rock_list.filter(miner_data__mine__state='PRK')
#             rock_perak_production = 0
#             rock_perak_royalties = 0
#             for rock in rock_perak_list:
#                 rock_perak_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_perak_royalties += rock.miner_data.royalties.royalties

#             rock_selangor_list = rock_list.filter(
#                 miner_data__mine__state='SGR')
#             rock_selangor_production = 0
#             rock_selangor_royalties = 0
#             for rock in rock_selangor_list:
#                 rock_selangor_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_selangor_royalties += rock.miner_data.royalties.royalties

#             rock_nsembilan_list = rock_list.filter(
#                 miner_data__mine__state='PLS')
#             rock_nsembilan_production = 0
#             rock_nsembilan_royalties = 0
#             for rock in rock_nsembilan_list:
#                 rock_nsembilan_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_nsembilan_royalties += rock.miner_data.royalties.royalties

#             rock_melaka_list = rock_list.filter(
#                 miner_data__mine__state='MLK')
#             rock_melaka_production = 0
#             rock_melaka_royalties = 0
#             for rock in rock_melaka_list:
#                 rock_melaka_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_melaka_royalties += rock.miner_data.royalties.royalties

#             rock_johor_list = rock_list.filter(miner_data__mine__state='JHR')
#             rock_johor_production = 0
#             rock_johor_royalties = 0
#             for rock in rock_johor_list:
#                 rock_johor_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_johor_royalties += rock.miner_data.royalties.royalties

#             rock_pahang_list = rock_list.filter(
#                 miner_data__mine__state='PHG')
#             rock_pahang_production = 0
#             rock_pahang_royalties = 0
#             for rock in rock_pahang_list:
#                 rock_pahang_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_pahang_royalties += rock.miner_data.royalties.royalties

#             rock_terengganu_list = rock_list.filter(
#                 miner_data__mine__state='TRG')
#             rock_terengganu_production = 0
#             rock_terengganu_royalties = 0
#             for rock in rock_terengganu_list:
#                 rock_terengganu_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_terengganu_royalties += rock.miner_data.royalties.royalties

#             rock_kelantan_list = rock_list.filter(
#                 miner_data__mine__state='KTN')
#             rock_kelantan_production = 0
#             rock_kelantan_royalties = 0
#             for rock in rock_kelantan_list:
#                 rock_kelantan_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_kelantan_royalties += rock.miner_data.royalties.royalties

#             rock_sarawak_list = rock_list.filter(
#                 miner_data__mine__state='SWK')
#             rock_sarawak_production = 0
#             rock_sarawak_royalties = 0
#             for rock in rock_sarawak_list:
#                 rock_sarawak_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_sarawak_royalties += rock.miner_data.royalties.royalties

#             rock_sabah_list = rock_list.filter(miner_data__mine__state='SBH')
#             rock_sabah_production = 0
#             rock_sabah_royalties = 0
#             for rock in rock_sabah_list:
#                 rock_sabah_production += rock.miner_data.productionstatistic.main_rock_production
#                 rock_sabah_royalties += rock.miner_data.royalties.royalties

#             rock = {
#                 'perlis': {
#                     'production': rock_perlis_production,
#                     'royalties': rock_perlis_royalties,
#                 },
#                 'kedah': {
#                     'production': rock_kedah_production,
#                     'royalties': rock_kedah_royalties,
#                 },
#                 'penang': {
#                     'production': rock_penang_production,
#                     'royalties': rock_penang_royalties,
#                 },
#                 'perak': {
#                     'production': rock_perak_production,
#                     'royalties': rock_perak_royalties,
#                 },
#                 'selangor': {
#                     'production': rock_selangor_production,
#                     'royalties': rock_selangor_royalties,
#                 },
#                 'nsembilan': {
#                     'production': rock_nsembilan_production,
#                     'royalties': rock_nsembilan_royalties,
#                 },
#                 'melaka': {
#                     'production': rock_melaka_production,
#                     'royalties': rock_melaka_royalties,
#                 },
#                 'johor': {
#                     'production': rock_johor_production,
#                     'royalties': rock_johor_royalties,
#                 },
#                 'pahang': {
#                     'production': rock_pahang_production,
#                     'royalties': rock_pahang_royalties,
#                 },
#                 'terengganu': {
#                     'production': rock_terengganu_production,
#                     'royalties': rock_terengganu_royalties,
#                 },
#                 'kelantan': {
#                     'production': rock_kelantan_production,
#                     'royalties': rock_kelantan_royalties,
#                 },
#                 'sarawak': {
#                     'production': rock_sarawak_production,
#                     'royalties': rock_sarawak_royalties,
#                 },
#                 'sabah': {
#                     'production': rock_sabah_production,
#                     'royalties': rock_sabah_royalties,
#                 },
#             }

#             return rock

#         rock1 = get_rock_list(rock1_list)
#         rock2 = get_rock_list(rock2_list)
#         rock3 = get_rock_list(rock3_list)
#         rock4 = get_rock_list(rock4_list)
#         rock5 = get_rock_list(rock5_list)

#         total_by_state = {
#             'perlis': {
#                 'production': sum([
#                     rock1['perlis']["production"],
#                     rock2['perlis']["production"],
#                     rock3['perlis']["production"],
#                     rock4['perlis']["production"],
#                     rock5['perlis']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['perlis']["royalties"],
#                     rock2['perlis']["royalties"],
#                     rock3['perlis']["royalties"],
#                     rock4['perlis']["royalties"],
#                     rock5['perlis']["royalties"],
#                 ]),
#             },
#             'kedah': {
#                 'production': sum([
#                     rock1['kedah']["production"],
#                     rock2['kedah']["production"],
#                     rock3['kedah']["production"],
#                     rock4['kedah']["production"],
#                     rock5['kedah']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['kedah']["royalties"],
#                     rock2['kedah']["royalties"],
#                     rock3['kedah']["royalties"],
#                     rock4['kedah']["royalties"],
#                     rock5['kedah']["royalties"],
#                 ]),
#             },
#             'penang': {
#                 'production': sum([
#                     rock1['penang']["production"],
#                     rock2['penang']["production"],
#                     rock3['penang']["production"],
#                     rock4['penang']["production"],
#                     rock5['penang']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['penang']["royalties"],
#                     rock2['penang']["royalties"],
#                     rock3['penang']["royalties"],
#                     rock4['penang']["royalties"],
#                     rock5['penang']["royalties"],
#                 ]),
#             },
#             'perak': {
#                 'production': sum([
#                     rock1['perak']["production"],
#                     rock2['perak']["production"],
#                     rock3['perak']["production"],
#                     rock4['perak']["production"],
#                     rock5['perak']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['perak']["royalties"],
#                     rock2['perak']["royalties"],
#                     rock3['perak']["royalties"],
#                     rock4['perak']["royalties"],
#                     rock5['perak']["royalties"],
#                 ]),
#             },
#             'selangor': {
#                 'production': sum([
#                     rock1['selangor']["production"],
#                     rock2['selangor']["production"],
#                     rock3['selangor']["production"],
#                     rock4['selangor']["production"],
#                     rock5['selangor']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['selangor']["royalties"],
#                     rock2['selangor']["royalties"],
#                     rock3['selangor']["royalties"],
#                     rock4['selangor']["royalties"],
#                     rock5['selangor']["royalties"],
#                 ]),
#             },
#             'nsembilan': {
#                 'production': sum([
#                     rock1['nsembilan']["production"],
#                     rock2['nsembilan']["production"],
#                     rock3['nsembilan']["production"],
#                     rock4['nsembilan']["production"],
#                     rock5['nsembilan']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['nsembilan']["royalties"],
#                     rock2['nsembilan']["royalties"],
#                     rock3['nsembilan']["royalties"],
#                     rock4['nsembilan']["royalties"],
#                     rock5['nsembilan']["royalties"],
#                 ]),
#             },
#             'melaka': {
#                 'production': sum([
#                     rock1['melaka']["production"],
#                     rock2['melaka']["production"],
#                     rock3['melaka']["production"],
#                     rock4['melaka']["production"],
#                     rock5['melaka']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['melaka']["royalties"],
#                     rock2['melaka']["royalties"],
#                     rock3['melaka']["royalties"],
#                     rock4['melaka']["royalties"],
#                     rock5['melaka']["royalties"],
#                 ]),
#             },
#             'johor': {
#                 'production': sum([
#                     rock1['johor']["production"],
#                     rock2['johor']["production"],
#                     rock3['johor']["production"],
#                     rock4['johor']["production"],
#                     rock5['johor']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['johor']["royalties"],
#                     rock2['johor']["royalties"],
#                     rock3['johor']["royalties"],
#                     rock4['johor']["royalties"],
#                     rock5['johor']["royalties"],
#                 ]),
#             },
#             'pahang': {
#                 'production': sum([
#                     rock1['pahang']["production"],
#                     rock2['pahang']["production"],
#                     rock3['pahang']["production"],
#                     rock4['pahang']["production"],
#                     rock5['pahang']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['pahang']["royalties"],
#                     rock2['pahang']["royalties"],
#                     rock3['pahang']["royalties"],
#                     rock4['pahang']["royalties"],
#                     rock5['pahang']["royalties"],
#                 ]),
#             },
#             'terengganu': {
#                 'production': sum([
#                     rock1['terengganu']["production"],
#                     rock2['terengganu']["production"],
#                     rock3['terengganu']["production"],
#                     rock4['terengganu']["production"],
#                     rock5['terengganu']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['terengganu']["royalties"],
#                     rock2['terengganu']["royalties"],
#                     rock3['terengganu']["royalties"],
#                     rock4['terengganu']["royalties"],
#                     rock5['terengganu']["royalties"],
#                 ]),
#             },
#             'kelantan': {
#                 'production': sum([
#                     rock1['kelantan']["production"],
#                     rock2['kelantan']["production"],
#                     rock3['kelantan']["production"],
#                     rock4['kelantan']["production"],
#                     rock5['kelantan']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['kelantan']["royalties"],
#                     rock2['kelantan']["royalties"],
#                     rock3['kelantan']["royalties"],
#                     rock4['kelantan']["royalties"],
#                     rock5['kelantan']["royalties"],
#                 ]),
#             },
#             'sarawak': {
#                 'production': sum([
#                     rock1['sarawak']["production"],
#                     rock2['sarawak']["production"],
#                     rock3['sarawak']["production"],
#                     rock4['sarawak']["production"],
#                     rock5['sarawak']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['sarawak']["royalties"],
#                     rock2['sarawak']["royalties"],
#                     rock3['sarawak']["royalties"],
#                     rock4['sarawak']["royalties"],
#                     rock5['sarawak']["royalties"],
#                 ]),
#             },
#             'sabah': {
#                 'production': sum([
#                     rock1['sabah']["production"],
#                     rock2['sabah']["production"],
#                     rock3['sabah']["production"],
#                     rock4['sabah']["production"],
#                     rock5['sabah']["production"],
#                 ]),
#                 'royalties': sum([
#                     rock1['sabah']["royalties"],
#                     rock2['sabah']["royalties"],
#                     rock3['sabah']["royalties"],
#                     rock4['sabah']["royalties"],
#                     rock5['sabah']["royalties"],
#                 ]),
#             },
#         }

#         states = [
#             {
#                 'name': 'PERLIS',
#                 'rock1': rock1['perlis'],
#                 'rock2': rock2['perlis'],
#                 'rock3': rock3['perlis'],
#                 'rock4': rock4['perlis'],
#                 'rock5': rock5['perlis'],
#                 'total_by_state': total_by_state['perlis'],
#             },
#             {
#                 'name': 'KEDAH',
#                 'rock1': rock1['kedah'],
#                 'rock2': rock2['kedah'],
#                 'rock3': rock3['kedah'],
#                 'rock4': rock4['kedah'],
#                 'rock5': rock5['kedah'],
#                 'total_by_state': total_by_state['kedah'],
#             },
#             {
#                 'name': 'PULAU PINANG',
#                 'rock1': rock1['penang'],
#                 'rock2': rock2['penang'],
#                 'rock3': rock3['penang'],
#                 'rock4': rock4['penang'],
#                 'rock5': rock5['penang'],
#                 'total_by_state': total_by_state['penang'],
#             },
#             {
#                 'name': 'PERAK',
#                 'rock1': rock1['perak'],
#                 'rock2': rock2['perak'],
#                 'rock3': rock3['perak'],
#                 'rock4': rock4['perak'],
#                 'rock5': rock5['perak'],
#                 'total_by_state': total_by_state['perak'],
#             },
#             {
#                 'name': 'SELANGOR',
#                 'rock1': rock1['selangor'],
#                 'rock2': rock2['selangor'],
#                 'rock3': rock3['selangor'],
#                 'rock4': rock4['selangor'],
#                 'rock5': rock5['selangor'],
#                 'total_by_state': total_by_state['selangor'],
#             },
#             {
#                 'name': 'NEGERI SEMBILAN',
#                 'rock1': rock1['nsembilan'],
#                 'rock2': rock2['nsembilan'],
#                 'rock3': rock3['nsembilan'],
#                 'rock4': rock4['nsembilan'],
#                 'rock5': rock5['nsembilan'],
#                 'total_by_state': total_by_state['nsembilan'],
#             },
#             {
#                 'name': 'MELAKA',
#                 'rock1': rock1['melaka'],
#                 'rock2': rock2['melaka'],
#                 'rock3': rock3['melaka'],
#                 'rock4': rock4['melaka'],
#                 'rock5': rock5['melaka'],
#                 'total_by_state': total_by_state['melaka'],
#             },
#             {
#                 'name': 'JOHOR',
#                 'rock1': rock1['johor'],
#                 'rock2': rock2['johor'],
#                 'rock3': rock3['johor'],
#                 'rock4': rock4['johor'],
#                 'rock5': rock5['johor'],
#                 'total_by_state': total_by_state['johor'],
#             },
#             {
#                 'name': 'PAHANG',
#                 'rock1': rock1['pahang'],
#                 'rock2': rock2['pahang'],
#                 'rock3': rock3['pahang'],
#                 'rock4': rock4['pahang'],
#                 'rock5': rock5['pahang'],
#                 'total_by_state': total_by_state['pahang'],
#             },
#             {
#                 'name': 'PERLIS',
#                 'rock1': rock1['terengganu'],
#                 'rock2': rock2['terengganu'],
#                 'rock3': rock3['terengganu'],
#                 'rock4': rock4['terengganu'],
#                 'rock5': rock5['terengganu'],
#                 'total_by_state': total_by_state['terengganu'],
#             },
#             {
#                 'name': 'KELANTAN',
#                 'rock1': rock1['kelantan'],
#                 'rock2': rock2['kelantan'],
#                 'rock3': rock3['kelantan'],
#                 'rock4': rock4['kelantan'],
#                 'rock5': rock5['kelantan'],
#                 'total_by_state': total_by_state['kelantan'],
#             },
#             {
#                 'name': 'SARAWAK',
#                 'rock1': rock1['sarawak'],
#                 'rock2': rock2['sarawak'],
#                 'rock3': rock3['sarawak'],
#                 'rock4': rock4['sarawak'],
#                 'rock5': rock5['sarawak'],
#                 'total_by_state': total_by_state['sarawak'],
#             },
#             {
#                 'name': 'SABAH',
#                 'rock1': rock1['sabah'],
#                 'rock2': rock2['sabah'],
#                 'rock3': rock3['sabah'],
#                 'rock4': rock4['sabah'],
#                 'rock5': rock5['sabah'],
#                 'total_by_state': total_by_state['sabah'],
#             },
#         ]

#         rocks = {
#             'rock1': {
#                 'name': rock_type1,
#                 'production': sum([state['rock1']['production'] for state in states]),
#             },
#             'rock2': {
#                 'name': rock_type2,
#                 'production': sum([state['rock2']['production'] for state in states]),
#             },
#             'rock3': {
#                 'name': rock_type3,
#                 'production': sum([state['rock3']['production'] for state in states]),
#             },
#             'rock4': {
#                 'name': rock_type4,
#                 'production': sum([state['rock4']['production'] for state in states]),
#             },
#             'rock5': {
#                 'name': rock_type5,
#                 'production': sum([state['rock5']['production'] for state in states]),
#             },
#         }

#         total = {
#             'production': sum([state['total_by_state']['production'] for state in states]),
#             'royalties': sum([state['total_by_state']['royalties'] for state in states]),
#         }

#         if month:
#             month = dict(form.fields['month'].choices)[int(month)]

#         context = {
#             'title': 'Laporan/Graph Lombong',
#             'form': form,
#             'year': year,
#             'month': month,
#             'rocks': rocks,
#             'states': states,
#             'total': total,
#         }

#         return render(request, 'report/hq/graph/mine/data.html', context)

#     context = {
#         'form': form,
#         'title': 'Laporan/Graph Lombong',
#     }

#     return render(request, 'report/hq/graph/mine/form.html', context)
