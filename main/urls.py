from django.urls import path

from main.views import *

urlpatterns = [
    path('', home, name='home'),
    path('statistics/<int:level>', Stat.as_view(), name='statistics'),
    path('load_data/', load_data, name='load_data'),
    path('data/<int:company_id>', Data.as_view(), name='data'),
]
