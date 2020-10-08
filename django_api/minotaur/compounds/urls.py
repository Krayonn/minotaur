from django.urls import path
from compounds.views import CompoundList, CompoundDetail, load_data

app_name = 'compound'

urlpatterns = [
    path('', CompoundList.as_view()),
    path('<int:pk>/', CompoundDetail.as_view()),
    path('load', load_data, name='load_data')
]
