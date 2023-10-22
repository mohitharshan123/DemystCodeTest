from django.contrib import admin
from django.urls import path, include
from .views import BalanceSheetView, DecisionView

urlpatterns = [
    path('balance_sheet/', BalanceSheetView.as_view()), 
    path('apply/', DecisionView.as_view(), name='apply'), 
]



