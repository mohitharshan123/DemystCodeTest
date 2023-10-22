from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime
from django.urls import reverse

from .models import Business, BalanceSheet

class BalanceSheetViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/balance_sheet/'  
        self.business_info = {
            'business_name': 'Rockstars',
            'year_established': 2010,
            'provider_name': 'Xero',  
            'loan_amount': 50000,  
        }
        current_year = datetime.now().year
        self.years_range = range(self.business_info['year_established'], current_year + 1)

    def test_balance_sheet_view(self):
        business = Business.objects.create(name=self.business_info['business_name'], year_established=self.business_info['year_established'])
        for year in self.years_range:
            for month in range(1, 13):
                balance_sheet = BalanceSheet.objects.create(
                    business=business,
                    year=year,
                    month=month,
                    profit_or_loss=10000,
                    assets_value=50000,
                )
        response = self.client.post(self.url, self.business_info, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        balance_sheet_data = response.data
        self.assertIn('balance_sheet', balance_sheet_data) 

    def test_invalid_data(self):
        invalid_data = {
            'business_name': '', 
            'year_established': 2010,
            'provider_name': 'Xero',
            'loan_amount': 50000,
        }
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unknown_provider(self):
        unknown_provider_info = self.business_info.copy()
        unknown_provider_info['provider_name'] = 'UnknownProvider'
        response = self.client.post(self.url, unknown_provider_info, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

class DecisionViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/apply/' 
        self.business_info = {
            'business_name': 'Demyst',
            'year_established': 2010,
            'provider_name': 'Xero',
            'loan_amount': 50000,
        }

    def test_decision_view_approval(self):
        business = Business.objects.create(name=self.business_info['business_name'], year_established=self.business_info['year_established'])

        for year in range(2010, 2023):
            for month in range(1, 13):
                balance_sheet = BalanceSheet.objects.create(
                    business=business,
                    year=year,
                    month=month,
                    profit_or_loss=10000,
                    assets_value=50000,
                )

        response = self.client.post(self.url, self.business_info, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        decision_data = response.data
        self.assertIn('status', decision_data)
        self.assertEqual(decision_data['status'], 'Approved') 
    
    def test_decision_view_rejection(self):
        business = Business.objects.create(name=self.business_info['business_name'], year_established=self.business_info['year_established'])

        for year in range(2010, 2023):
            for month in range(1, 13):
                balance_sheet = BalanceSheet.objects.create(
                    business=business,
                    year=year,
                    month=month,
                    profit_or_loss=-2000,
                    assets_value=0,
                )

        response = self.client.post(self.url, self.business_info, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        decision_data = response.data
        self.assertIn('status', decision_data)
        self.assertEqual(decision_data['status'], 'Rejected') 


    def test_invalid_data(self):
        invalid_data = {
            'business_name': '', 
            'year_established': 2010,
            'provider_name': 'Xero',
            'loan_amount': 50000,
        }
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
