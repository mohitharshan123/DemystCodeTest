import json
from django.core.management.base import BaseCommand
from accounting.models import Business, BalanceSheet 

class Command(BaseCommand):
    help = 'Seed data for businesses with balance sheets'

    def handle(self, *args, **options):
        business_names = ["Rockstars", "Demyst", "EY"]
        dummy_data = []

        for i, business_name in enumerate(business_names):
            business = Business(name=business_name, year_established=2010 + i)
            business.save()

            for year in range(2010, 2023):
                for month in range(1, 13):  # Loop through months from 1 to 12
                    balance_sheet = BalanceSheet(
                        business=business,
                        year=year,
                        month=month,
                        profit_or_loss=250000, 
                        assets_value=1234, 
                    )
                    balance_sheet.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded data for multiple businesses.'))
