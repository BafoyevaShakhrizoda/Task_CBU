from datetime import datetime 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Currency, CurrencyRate
from .serializers import CurrencySerializer, CurrencyRateSerializer, ConvertRequestSerializer


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def get_rates_from_db(target_date):
    rates = CurrencyRate.objects.filter(created_at__date=target_date)
    return rates

def get(self, request):
        target_date = parse_date(request.query_params.get("date"))
        rates = get_rates_from_db(target_date)

        return Response({
            "success": True,
            "date": target_date.strftime("%Y-%m-%d"),
            "source": "CBU (cbu.uz)",
            "count": len(rates),
            "rates": list(rates.values()),
        })

class CurrencyListAPIView(APIView):
    def get(self, request):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ConvertAPIView(APIView):
    def post(self, request):
        serializer = ConvertRequestSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            from_currency_code = serializer.validated_data['from_currency']
            to_currency_code = serializer.validated_data['to_currency']
            date = serializer.validated_data['date']

            try:
                from_currency = Currency.objects.get(code=from_currency_code)
                to_currency = Currency.objects.get(code=to_currency_code)
            except Currency.DoesNotExist:
                return Response({'error': 'Currency not found'}, status=status.HTTP_404_NOT_FOUND)

            try:
                from_rate = from_currency.rates.filter(created_at__date=date).latest('created_at').rate
                to_rate = to_currency.rates.filter(created_at__date=date).latest('created_at').rate
            except CurrencyRate.DoesNotExist:
                return Response({'error': 'Currency rate not found for the specified date'}, status=status.HTTP_404_NOT_FOUND)

            converted_amount = (amount / from_rate) * to_rate
            return Response({'converted_amount': converted_amount}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 


