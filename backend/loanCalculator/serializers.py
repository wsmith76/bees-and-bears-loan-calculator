import re  # Import the regular expression module

from rest_framework import serializers  # Import the serializers module from Django REST framework
from .models import Customer, LoanOffer  # Import the Customer and LoanOffer models from the current module

# Serializer for the LoanOffer model
class LoanOfferSerializer(serializers.ModelSerializer):
    # Field to relate LoanOffer to Customer via primary key
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer')

    # Meta class to define model and fields to be included in the serialization
    class Meta:
        model = LoanOffer
        fields = ['id', 'customer_id', 'amount', 'interest_rate', 'term_in_months', 'monthly_payments']

    # Validation for the amount field
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("The loan amount must be greater than zero.")
        return value

    # Validation for the interest rate field
    def validate_interest_rate(self, value):
        if value < 0:
            raise serializers.ValidationError("The interest rate cannot be negative.")
        return value

    # Validation for the term in months field
    def validate_term_in_months(self, value):
        if value <= 0:
            raise serializers.ValidationError("The term must be greater than zero months.")
        return value

# Serializer for the Customer model
class CustomerSerializer(serializers.ModelSerializer):
    # Custom field to include loan offers related to the customer
    loan_offers = LoanOfferSerializer(many=True, read_only=True)

    # Meta class to define model and fields to be included in the serialization
    class Meta:
        model = Customer
        fields = [
            'id', 'first_name', 'last_name', 'street', 'house_number',
            'city', 'state', 'postal_code', 'phone_number', 'email',
            'loan_offers'
        ]

    # Validation for the first name field
    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError("First name is required.")
        return value

    # Validation for the last name field
    def validate_last_name(self, value):
        if not value:
            raise serializers.ValidationError("Last name is required.")
        return value

    # Validation for the email field
    def validate_email(self, value):
        # Ensure the email is not empty and follows a basic email pattern
        if not value or not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("A valid email address is required.")
        return value

    # Validation for the phone number field
    def validate_phone_number(self, value):
        # Ensure the phone number is not empty and follows a German phone number pattern
        if not value or not re.match(r"^(?:\+49|0)(\s?\d+|\(\d+\))[\s\-]?\d+[\s\-]?\d+$", value):
            raise serializers.ValidationError("A valid German phone number is required.")
        return value

    # Validation for the postal code field
    def validate_postal_code(self, value):
        # Ensure the postal code follows the German postal code pattern of five digits
        if not re.match(r'^\d{5}$', value):
            raise serializers.ValidationError("A valid postal code is required.")
        return value


