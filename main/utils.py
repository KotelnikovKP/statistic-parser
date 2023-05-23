from datetime import datetime, date, timedelta
from random import choice

from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlencode

from main.models import *


def get_date(date_quantity):
    previous_month_day = datetime(date.today().year, date.today().month, 1) - timedelta(days=1)
    year = previous_month_day.year
    month = previous_month_day.month
    n = choice([0, 1, 2]) if date_quantity == 3 else choice([0, 1]) if date_quantity == 2 else 0
    day = (n % 3) * 10 + 1 if date_quantity == 3 else (n % 2) * 15 + 1 if date_quantity == 2 else 1
    return date(year, month, day)


def get_float(value):
    try:
        result = float(value)
    except Exception as e:
        result = 0.0
    return result


def get_u_context(request, initial_context):
    context = initial_context

    companies = Company.objects.all().order_by('name')
    context['companies'] = companies

    if 'company_selected' not in context:
        context['company_selected'] = 0

    if 'indicators_level_selected' not in context:
        context['indicators_level_selected'] = 1

    return context


class SafePaginator(Paginator):
    def validate_number(self, number):
        try:
            return super(SafePaginator, self).validate_number(number)
        except EmptyPage:
            if number > 1:
                return self.num_pages
            else:
                raise


class DataMixin:
    paginator_class = SafePaginator
    paginate_by = 20

    def get_user_context(self, **kwargs):
        return get_u_context(self.request, kwargs)


def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name, args=args)
    params = urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)

