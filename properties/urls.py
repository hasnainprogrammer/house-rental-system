from django.urls import path
from . import views

urlpatterns = [
    path('', views.properties, name='properties'),
    path('property/<int:property_id>', views.property, name='property'),
    path('search_property', views.search_property, name='search_property'),  
]