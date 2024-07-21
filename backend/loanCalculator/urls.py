from django.urls import path
from .views import CustomerCreateView, CustomerDetailView, LoanOfferCreateView

urlpatterns = [
    path('customers', CustomerCreateView.as_view(), name='customer-create'),
    path('customers/<int:id>', CustomerDetailView.as_view(), name='customer-detail'),
    path('loanoffers', LoanOfferCreateView.as_view(), name='loanoffer-create'),
]
