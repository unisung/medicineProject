"""
URL configuration for medicine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('map_view/',                  views.map_view,                  name='map_view'),
    path('map_visualization/',         views.map_visualization,         name='map_visualization'),
    path('map_population/',            views.map_population,            name='map_population'),
    path('district_graph/',            views.district_graph,            name='district_graph'),
    path('district_pie_chart/',        views.district_pie_chart,        name='district_pie_chart'),
    path('district_distribution/',     views.district_distribution,     name='district_distribution'),
    path('medical_institution_types/', views.medical_institution_types, name='medical_institution_types'),
    path('district_total_doctors/',    views.district_total_doctors,    name='district_total_doctors'),
    path('map_view_hospitals/<str:district>/',        views.map_view_hospitals,        name='map_view_hospitals'),
]
