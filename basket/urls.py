from django.urls import path

from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.basketSummary, name='basket_summary'),
    path('add/', views.basketAdd, name='basket_add'),
    path('delete/', views.basketDelete, name='basket_delete'),
    path('update/', views.basketUpdate, name='basket_update'),
]
