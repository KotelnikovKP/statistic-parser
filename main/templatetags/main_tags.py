from django import template

register = template.Library()

main_menu = [
    {'title': "Статистика", 'url_name': 'statistics', 'url_suffix': 2},
    {'title': "Загрузить данные", 'url_name': 'load_data'},
    {'title': "Посмотреть данные", 'url_name': 'data', 'url_suffix': 0},
]


@register.inclusion_tag('main/menu_main.html')
def show_main_menu():
    return {"menu": main_menu}


@register.inclusion_tag('main/menu_home.html')
def show_home_left_menu():
    return {"menu": main_menu}


@register.inclusion_tag('main/menu_statistics.html')
def show_statistics_left_menu(indicators_level_selected=None):
    return {'indicators_level_selected': indicators_level_selected}


@register.inclusion_tag('main/menu_data.html')
def show_data_left_menu(company_selected=None, companies=None):
    return {'company_selected': company_selected, 'companies': companies}


@register.simple_tag
def url_replace(request, field, value):
    d = request.GET.copy()
    d[field] = value
    return d.urlencode()


@register.simple_tag(name='get_width')
def get_width(value):
    if value < 1000:
        width = 30
    elif value < 10000:
        width = 40
    elif value < 100000:
        width = 50
    elif value < 1000000:
        width = 60
    else:
        width = 70
    return width


