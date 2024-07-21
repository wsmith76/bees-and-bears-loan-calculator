from django.test import TestCase
from ..models import Customer, LoanOffer
from ..serializers import CustomerSerializer, LoanOfferSerializer
import decimal

class CustomerSerializerTestCase(TestCase):

    def setUp(self):
        self.customer_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'street': 'Main Street',
            'house_number': '123',
            'city': 'Berlin',
            'state': 'Berlin',
            'postal_code': '10115',
            'phone_number': '+491234567890',
            'email': 'john.doe@example.com'
        }
        self.customer = Customer.objects.create(**self.customer_data)

    def tearDown(self):
        Customer.objects.all().delete()

    def test_customer_serializer_valid(self):
        serializer = CustomerSerializer(instance=self.customer)
        self.assertEqual(serializer.data['first_name'], 'John')

    def test_customer_serializer_invalid_email(self):
        invalid_data = self.customer_data.copy()
        invalid_data['email'] = 'invalid-email'
        serializer = CustomerSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_customer_serializer_invalid_phone_number(self):
        invalid_data = self.customer_data.copy()
        invalid_data['phone_number'] = '12345'
        serializer = CustomerSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('phone_number', serializer.errors)

    def test_customer_serializer_invalid_postal_code(self):
        invalid_data = self.customer_data.copy()
        invalid_data['postal_code'] = 'ABCDE'
        serializer = CustomerSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('postal_code', serializer.errors)


class LoanOfferSerializerTestCase(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='Jane',
            last_name='Doe',
            street='Main Street',
            house_number='123',
            city='Berlin',
            state='Berlin',
            postal_code='10115',
            phone_number='+491234567890',
            email='jane.doe@example.com'
        )
        self.loan_offer_data = {
            'customer': self.customer,
            'amount': decimal.Decimal('5000.00'),
            'interest_rate': decimal.Decimal('5.5'),
            'term_in_months': 24
        }
        self.loan_offer = LoanOffer.objects.create(**self.loan_offer_data)

    def tearDown(self):
        LoanOffer.objects.all().delete()
        Customer.objects.all().delete()

    def test_loan_offer_serializer_valid(self):
        serializer = LoanOfferSerializer(instance=self.loan_offer)
        self.assertEqual(serializer.data['amount'], '5000.00')
        self.assertIn('monthly_payments', serializer.data)

    def test_loan_offer_serializer_invalid_amount(self):
        invalid_data = self.loan_offer_data.copy()
        invalid_data['amount'] = -100
        serializer = LoanOfferSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('amount', serializer.errors)

    def test_loan_offer_serializer_invalid_interest_rate(self):
        invalid_data = self.loan_offer_data.copy()
        invalid_data['interest_rate'] = -1
        serializer = LoanOfferSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('interest_rate', serializer.errors)

    def test_loan_offer_serializer_invalid_term_in_months(self):
        invalid_data = self.loan_offer_data.copy()
        invalid_data['term_in_months'] = 0
        serializer = LoanOfferSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('term_in_months', serializer.errors)
