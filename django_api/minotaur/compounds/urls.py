from django.urls import path
from compounds.views import CompoundList, CompoundDetail, AssayList, AssayDetail, load_data

app_name = 'compound'

urlpatterns = [
    path('', CompoundList.as_view()),
    path('<int:compound_id>/', CompoundDetail.as_view()),
    path('<int:compound_id>/assays', AssayList.as_view()),
    path('<int:compound_id>/assays/<int:result_id>', AssayDetail.as_view()),
    path('load', load_data, name='load_data')
]
