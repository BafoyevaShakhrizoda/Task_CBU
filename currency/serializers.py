from rest_framework import serializers
from datetime import date

from .models import Currency, CurrencyRate


class ConvertRequestSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=20, decimal_places=6,
        help_text = 'Konvert qilmoqchi bolgan summangiz'
        )
    from_currency = serializers.ChaeField(
        max_length=10,
        help_text = 'Kiritmoqchi bolgan valyutangiz kodi (masalan, USD, UZS)',
    )
    to_currency = serializers.Charfield(
        max_length=10,
        help_text = 'Qaysi valyutaga konvert qilmoqchi ekanligingiz kodi (masalan, USD, UZS)',
    )
    date = serializers.DateField(
        default=date.today,
    )

    def validate_from_currency(self, value):
        return value.upper()

    def validate_to_currency(self, value):
        return value.upper()
    



# class CurrencySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Currency 
#         fields = '__all__'
#         help_texts = {
#             'name': "Name of the currency",
#             'code': "Currency uchun unuque kod (masalan, USD, UZS)",
#             'symbol': "Currency uchun simbol (masalan, $, so'm)",
#         }




class CurrencyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyRate
        fields = '__all__'
      
