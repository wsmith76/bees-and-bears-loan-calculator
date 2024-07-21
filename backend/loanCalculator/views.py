from rest_framework import generics  # Import generic class-based views from Django REST framework
from .models import Customer, LoanOffer  # Import the Customer and LoanOffer models from the current module
from .serializers import CustomerSerializer, LoanOfferSerializer  # Import the Customer and LoanOffer serializers

# View for creating a new Customer
class CustomerCreateView(generics.CreateAPIView):
    queryset = Customer.objects.all()  # Define the queryset to be all Customer objects
    serializer_class = CustomerSerializer  # Specify the serializer class to be used for this view

# View for retrieving details of a Customer
class CustomerDetailView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()  # Define the queryset to be all Customer objects
    serializer_class = CustomerSerializer  # Specify the serializer class to be used for this view
    lookup_field = 'id'  # Define the lookup field to be 'id' for retrieving customer details by ID

# View for creating a new LoanOffer
class LoanOfferCreateView(generics.CreateAPIView):
    queryset = LoanOffer.objects.all()  # Define the queryset to be all LoanOffer objects
    serializer_class = LoanOfferSerializer  # Specify the serializer class to be used for this view
