import decimal  # Module for fixed-point and floating-point arithmetic
import re  # Module for regular expression operations

from django.db import models  # Django module for database models
from django.core.exceptions import ValidationError  # Django exception for validation errors

class Customer(models.Model):
    id = models.AutoField(primary_key=True)  # Primary key field that auto-increments
    first_name = models.CharField(max_length=100)  # First name field with a maximum length of 100 characters
    last_name = models.CharField(max_length=100)  # Last name field with a maximum length of 100 characters
    street = models.CharField(max_length=255)  # Street address field with a maximum length of 255 characters
    house_number = models.CharField(max_length=10)  # House number field with a maximum length of 10 characters
    postal_code = models.CharField(max_length=10)  # Postal code field with a maximum length of 10 characters
    city = models.CharField(max_length=100)  # City field with a maximum length of 100 characters
    state = models.CharField(max_length=100)  # State field with a maximum length of 100 characters
    phone_number = models.CharField(max_length=15)  # Phone number field with a maximum length of 15 characters
    email = models.EmailField(unique=True)  # Email field that must be unique

    def clean(self):
        # Ensure first name is provided
        if not self.first_name:
            raise ValidationError("First name is required.")

        # Ensure last name is provided
        if not self.last_name:
            raise ValidationError("Last name is required.")

        # Ensure email is valid
        if not self.email or not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValidationError("A valid email address is required.")

        # Ensure phone number is a valid German phone number
        if not self.phone_number or not re.match(r"^(?:\+49|0)(\s?\d+|\(\d+\))[\s\-]?\d+[\s\-]?\d+$", self.phone_number):
            raise ValidationError("A valid German phone number is required.")

        # Ensure postal code follows the German postal code pattern of five digits
        if not re.match(r'^\d{5}$', self.postal_code):
            raise ValidationError("A valid postal code is required.")

    def normalize_phone_number(self):
        # Normalize phone number to the format +49XXXXXXXXXX
        if self.phone_number:
            # Remove spaces, hyphens, and parentheses
            normalized_number = re.sub(r'[()\s-]', '', self.phone_number)
            # Ensure the number starts with +49
            if not normalized_number.startswith('+49'):
                normalized_number = '+49' + normalized_number.lstrip('0')
            self.phone_number = normalized_number

    def save(self, *args, **kwargs):
        self.clean()  # Perform validation checks
        self.normalize_phone_number()  # Normalize the phone number before saving the model
        super().save(*args, **kwargs)  # Call the parent class's save method

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # String representation of the Customer instance



class LoanOffer(models.Model):
    id = models.AutoField(primary_key=True)  # Primary key field that auto-increments
    customer = models.ForeignKey(Customer, related_name='loan_offers', on_delete=models.CASCADE)  # Foreign key to Customer
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Loan amount with up to 10 digits and 2 decimal places
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Interest rate with up to 5 digits and 2 decimal places
    term_in_months = models.IntegerField()  # Loan term in months

    class Meta:
        # Ensure unique loan offer based on customer, amount, interest rate, and term
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'amount', 'interest_rate', 'term_in_months'],
                name='unique_loan_offer'
            )
        ]

    def monthly_payments(self):
        # Calculate the monthly payments using the loan amortization formula:
        # M = P * [r(1+r)^n] / [(1+r)^n - 1]
        # where P = loan amount, r = monthly interest rate, n = term in months

        P = self.amount
        r = (self.interest_rate / 100) / 12  # Convert annual rate percentage to a monthly decimal
        n = self.term_in_months
        if r == 0:  # Special case to handle zero interest loans
            return P / n
        factor = decimal.Decimal((1 + r) ** n)
        monthly = P * (r * factor) / (factor - 1)
        return monthly.quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_HALF_UP)  # Round to two decimal places

    def clean(self):
        # Ensure loan amount is greater than zero
        if self.amount <= 0:
            raise ValidationError("The loan amount must be greater than zero.")
        # Ensure interest rate is not negative
        if self.interest_rate < 0:
            raise ValidationError("The interest rate cannot be negative.")
        # Ensure term is greater than zero months
        if self.term_in_months <= 0:
            raise ValidationError("The term must be greater than zero months.")

    def save(self, *args, **kwargs):
        self.clean()  # Perform validation checks
        super().save(*args, **kwargs)  # Call the parent class's save method

    def __str__(self):
        return f"Loan Offer {self.id} for {self.customer}"  # String representation of the LoanOffer instance
