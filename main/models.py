from django.db import models
from django.db.models import Index

LEVELS = [
    (1, 'Первый уровень'),
    (2, 'Второй уровень'),
    (3, 'Третий уровень'),
]


class Indicator(models.Model):
    """
        Индикатор
    """
    name = models.CharField(max_length=100, db_index=True, verbose_name='Наименование')
    level = models.IntegerField(verbose_name='Уровень', choices=LEVELS, default=1, null=False, blank=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Индикатор'
        verbose_name_plural = 'Индикаторы'
        ordering = ['level', 'name']
        indexes = (Index(fields=['level', 'name'], name='indicator_level_name_idx'),)


class Company(models.Model):
    """
        Компания
    """
    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='Наименование')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['name']


class Statistics(models.Model):
    stats_date = models.DateField(null=False, blank=False, db_index=True, verbose_name='Дата замера')
    company = models.ForeignKey('Company', on_delete=models.PROTECT, verbose_name='Компания')
    first_level_indicator = models.ForeignKey('Indicator', on_delete=models.PROTECT, null=False,
                                              blank=False, related_name='first_level_statistics',
                                              verbose_name='Индикатор первого уровня')
    second_level_indicator = models.ForeignKey('Indicator', on_delete=models.PROTECT, null=False,
                                               blank=False, related_name='second_level_statistics',
                                               verbose_name='Индикатор второго уровня')
    third_level_indicator = models.ForeignKey('Indicator', on_delete=models.PROTECT, null=False,
                                              blank=False, related_name='third_level_statistics',
                                              verbose_name='Индикатор третьего уровня')
    value = models.FloatField(null=False, blank=False, verbose_name='Значение')

    def __str__(self):
        return f"{self.stats_date}, {self.company}, {self.first_level_indicator}, {self.second_level_indicator}, " \
               f"{self.third_level_indicator}: {self.value}"

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'
        ordering = ['stats_date']
