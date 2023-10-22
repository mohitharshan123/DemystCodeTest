from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .helpers.accounting_provider import AccountingProviderHelper, UnsupportedProviderError
from .helpers.decision_engine import DecisionEngine
from .serializers import BusinessInfoSerializer, DecisionDataSerializer

class BaseBusinessView(APIView):
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            business_name = serializer.validated_data['business_name']
            year_established = serializer.validated_data['year_established']
            provider_name = serializer.validated_data['provider_name']
            loan_amount = serializer.validated_data['loan_amount']

            try:
                accounting_provider = AccountingProviderHelper(provider_name, business_name, loan_amount, year_established)
                response_data = self.process_request(accounting_provider, serializer)
                return Response(response_data, status=status.HTTP_200_OK)
            except UnsupportedProviderError as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BalanceSheetView(BaseBusinessView):
    serializer_class = BusinessInfoSerializer

    def process_request(self, accounting_provider, serializer):
        balance_sheet = accounting_provider.fetch_balance_sheet()
        return balance_sheet

class DecisionView(BaseBusinessView):
    serializer_class = DecisionDataSerializer

    def process_request(self, accounting_provider, serializer):
        pre_assessment = accounting_provider.calculate_pre_assessment()
        decision = DecisionEngine(
            pre_assessment["business_name"], 
            pre_assessment["year_established"], 
            pre_assessment["profit_or_loss_summary"],
            pre_assessment["pre_assessment_value"]).decide()
        return {'status': decision}
