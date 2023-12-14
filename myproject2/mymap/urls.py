from django.urls import path
from .views import map_view, hospital_chart, seoul_hospital_plots, seoul_doctors_charts, combined_pie_charts

urlpatterns = [
    path('map/', map_view, name='map'),
    path('hospital_chart/', hospital_chart, name='hospital_chart'),
    path('seoul_hospital_plots/', seoul_hospital_plots, name='seoul_hospital_plots'),
    path('seoul_doctors_charts/', seoul_doctors_charts, name='seoul_doctors_charts'),
    path('combined_pie_charts/', combined_pie_charts, name='combined_pie_charts'),  
]
