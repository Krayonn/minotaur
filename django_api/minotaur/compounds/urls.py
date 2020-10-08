from django.urls import path
from compounds.views import CompoundList, CompoundDetail, AssayList, AssayDetail, load_data

app_name = 'compound'

urlpatterns = [
    path('', CompoundList.as_view()),
    path('<int:c_pk>/', CompoundDetail.as_view()),
    path('<int:c_pk>/assays', AssayList.as_view()),
    path('<int:c_pk>/assays/<int:a_pk>', AssayDetail.as_view()),
    path('load', load_data, name='load_data')
]
