from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Currency(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique = True)
    symbol = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'  


class CurrencyRate(BaseModel):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='rates')
    rate = models.DecimalField(max_digits=20, decimal_places=6)
    
    
    
    def __str__(self):
        return f"{self.currency.code} - {self.rate}"
    
    class Meta:
        verbose_name = 'Currency Rate'
        verbose_name_plural = 'Currency Rates'


