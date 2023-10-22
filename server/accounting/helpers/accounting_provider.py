import datetime
from datetime import datetime
from django.db.models import Sum

from accounting.models import BalanceSheet


class UnsupportedProviderError(Exception):
    pass

class AccountingProviderHelper:
    def __init__(self, provider_name, business_name, loan_amount, year_established):
        self.provider_name = provider_name
        self.business_name = business_name
        self.loan_amount = loan_amount
        self.year_established = year_established

    def fetch_balance_sheet(self):
        provider_helper = self._get_provider_helper()
        balance_sheet = provider_helper.fetch_balance_sheet_data()
        return balance_sheet
    
    def calculate_pre_assessment(self):
        balance_sheets = BalanceSheet.objects.filter(business__name=self.business_name)

        last_12_months_data = balance_sheets.order_by('-year')[:12]

        total_profit_or_loss = last_12_months_data.aggregate(Sum('profit_or_loss'))['profit_or_loss__sum'] or 0
        total_assets_value = last_12_months_data.aggregate(Sum('assets_value'))['assets_value__sum'] or 0

        average_assets_value = total_assets_value / 12 if last_12_months_data else 0
        if average_assets_value > self.loan_amount:
            pre_assessment_value = 100
        elif total_profit_or_loss > 0:
            pre_assessment_value = 60
        else:
            pre_assessment_value = 20

        return {
                "business_name": self.business_name,
                "year_established": self.year_established,
                "profit_or_loss_summary": total_profit_or_loss,
                "pre_assessment_value": pre_assessment_value,
            }
 

    def _get_provider_helper(self):
        if self.provider_name == "Xero":
            return XeroHelper(self.business_name, self.year_established, self.loan_amount)
        elif self.provider_name == "MYOB":
            return MYOBHelper(self.business_name, self.year_established, self.loan_amount)
        else:
            raise UnsupportedProviderError(f"Unsupported provider name: {self.provider_name}")

class AccountingSoftwareWrapper:
    def __init__(self, business_name, year_established, loan_amount):
        self.business_name = business_name
        self.year_established = year_established
        self.loan_amount = loan_amount

    def fetch_balance_sheet_data(self):
        balance_sheet = list(BalanceSheet.objects.filter(business__name=self.business_name).values(
        'year', 'month', 'profit_or_loss', 'assets_value'))
        return { 'balance_sheet': balance_sheet}
 

class XeroHelper(AccountingSoftwareWrapper):
    pass
     
class MYOBHelper(AccountingSoftwareWrapper):
    pass
