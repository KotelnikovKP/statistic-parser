from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from main.forms import LoadDataForm
from main.models import Company, Statistics, Indicator
from main.parser import DataFileParser
from main.utils import get_u_context, DataMixin, get_float, get_date


def home(request):
    return render(
        request,
        'main/index.html',
        get_u_context(
            request,
            {'title': 'Парсер статистических данных',
             'home_menu': True,
             }
        )
    )


class Stat(DataMixin, ListView):
    """
        Класс-представление вывода статистики (выдает результат, запрошенный в задании)

        Получает на вход уровень индикаторов, до которого нужно произвести группировку:
        - 1 уровень: до индикаторов в первой строчке заголовка входного файла (в примере это fact и forecast)
        - 2 уровень: до индикаторов во второй строчке заголовка входного файла (в примере это Qliq и Qoil)
        - 3 уровень: до индикаторов в третьей строчке заголовка входного файла (в примере это data1 и data2)

        Изначально параметры группировки включают Компанию и Дату, затем к ним добавляются Индикаторы
        до заданного уровня.
    """
    model = Statistics
    template_name = 'main/statistics.html'
    context_object_name = 'statistics'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Статистика',
                                      statistics_menu=True,
                                      indicators_level_selected=self.kwargs['level'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        level = self.kwargs['level']
        statistics_qs = None

        # Определить QuerySet с группировкой в соответствие с заданным уровнем индикаторов
        if level == 1:
            statistics_qs = (
                Statistics.objects
                .values('company__name', 'stats_date', 'first_level_indicator__name')
                .annotate(total=Sum('value'))
                .order_by('company__name', 'stats_date', 'first_level_indicator__name')
            )
        elif level == 2:
            statistics_qs = (
                Statistics.objects
                .values('company__name', 'stats_date', 'first_level_indicator__name', 'second_level_indicator__name')
                .annotate(total=Sum('value'))
                .order_by('company__name', 'stats_date', 'first_level_indicator__name', 'second_level_indicator__name')
            )
        elif level == 3:
            statistics_qs = (
                Statistics.objects
                .values('company__name', 'stats_date', 'first_level_indicator__name', 'second_level_indicator__name',
                        'third_level_indicator__name')
                .annotate(total=Sum('value'))
                .order_by('company__name', 'stats_date', 'first_level_indicator__name', 'second_level_indicator__name',
                          'third_level_indicator__name')
            )
        return statistics_qs


def load_data(request):
    """
        Функция представления загрузки данный из входного файла

        Получает на вход:
        - Входной файл (*.xlxs)
        - Что делать с уже существующими данными в системе [Удалить, Оставить]
        - Сколько дат добавить [Одну (1-е число), Две (1-е и 16-е числа), Три (1-е, 11-е и 21-е числа)]:
            - все загруженные из входного файла данные получают рандомную дату предыдущего месяца
              в соответствие с выбором

        Алгоритм парсинга (класс parser.DataFileParser):
        1) проверка на валидность файла:
            - тип файла (это вообще excel)
            - структура файла:
                - наличие первых двух колонок 'id' и 'company'
                - наличие первых трех строчек с индикаторами
            - наличие данных в файле (индикаторы и значения)
        2) определение для каждой колонки трех индикаторов (1-го, 2-го и 3-го уровней, каждый из своей строчки)
        3) построение итератора, который на каждой итерации возвращает единичное значение,
           соответствующее набору параметров (id, company, индикатор 1-го уровня,
           индикатор 2-го уровня, индикатор 3-го уровня)

        После парсинга идет цикл по созданному итератору с сохранением данных в базу данных:
        - данные сохраняются в модель models.Statistics
        - при этом создается или берется существующая компания из входного параметра
        - также и с индикаторами всех уровней: создается или берется существующий
        - дата определяется рандомно в соответствие с входным параметром

        Перед сохранением новых данных предыдущие данные в моделе models.Statistics удаляются / не трогаются
        в соответствие с входным параметром
    """
    if request.method == 'POST':
        form = LoadDataForm(data=request.POST, files=request.FILES)

        if form.is_valid():

            # Произвести парсинг входного файла
            rows = DataFileParser(request.FILES['data_file'])
            if rows.valid:
                with transaction.atomic():

                    # Удалить существующие данный, если указано
                    if request.POST.get('what_is_with_data', '_') == 'delete':
                        Statistics.objects.all().delete()

                    # Выполнить цикл по итератору парсера
                    for row in rows:
                        try:
                            # Создать новый объект Statistics
                            statistics = Statistics(
                                stats_date=get_date(int(request.POST.get('date_quantity', 3))),
                                company=Company.objects.get_or_create(name=row['company'])[0],
                                first_level_indicator=
                                Indicator.objects.get_or_create(name=row['first_level_indicator'], level=1)[0],
                                second_level_indicator=
                                Indicator.objects.get_or_create(name=row['second_level_indicator'], level=2)[0],
                                third_level_indicator=
                                Indicator.objects.get_or_create(name=row['third_level_indicator'], level=3)[0],
                                value=get_float(row['value'])
                            )
                            # Сохранить новый объект Statistics
                            statistics.save()

                        except Exception as e:
                            print(e)

                # Перейти в представление просмотра данных
                return redirect('data', 0)

            else:
                form.add_error('data_file', rows.status)

    else:
        form = LoadDataForm()

    return render(
        request,
        'main/load_data.html',
        get_u_context(
            request,
            {'title': 'Загрузка данных из файла',
             'form': form,
             'load_data_menu': True,
             }
        )
    )


class Data(DataMixin, ListView):
    """
        Класс представление просмотра существующих данных из модели models.Statistics

        Получает на вход id компании (для фильтра данных по ней), либо 0 (для вывода данных по всем компаниям)
    """
    model = Statistics
    template_name = 'main/data.html'
    context_object_name = 'statistics'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.kwargs['company_id']:
            title = 'Просмотр всех загруженных данных'
        else:
            title = 'Просмотр загруженных данных по компании: ' + \
                    str(get_object_or_404(Company, pk=self.kwargs['company_id']))
        c_def = self.get_user_context(title=title,
                                      data_menu=True,
                                      company_selected=self.kwargs['company_id'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        if not self.kwargs['company_id']:
            qs = Statistics.objects.all().order_by('id')
        else:
            qs = Statistics.objects.filter(company_id=self.kwargs['company_id']).order_by('id')
        return qs
