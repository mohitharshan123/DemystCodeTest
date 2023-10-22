from rest_framework import serializers

class BusinessInfoSerializer(serializers.Serializer):
    business_name = serializers.CharField(max_length=100)
    year_established = serializers.IntegerField()
    provider_name = serializers.CharField()
    loan_amount = serializers.IntegerField()


class DecisionDataSerializer(BusinessInfoSerializer):
    pass
 