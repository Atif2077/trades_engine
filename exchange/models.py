from django.db import models
from django.contrib.auth.models import User

class Asset(models.Model):
    tkr = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    prc = models.DecimalField(max_digits=12, decimal_places=2)

class Wallet(models.Model):
    usr = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wlt")
    bal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

class Order(models.Model):
    TYP_CHOICES = [("MARKET", "Market"), ("LIMIT", "Limit")]
    ACT_CHOICES = [("BUY", "Buy"), ("SELL", "Sell")]
    ST_CHOICES = [("PENDING", "Pending"), ("FILLED", "Filled"), ("FAILED", "Failed")]

    usr = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ords")
    ast = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="ords")
    typ = models.CharField(max_length=10, choices=TYP_CHOICES)
    act = models.CharField(max_length=10, choices=ACT_CHOICES)
    qty = models.IntegerField()
    lmt_prc = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    st = models.CharField(max_length=10, choices=ST_CHOICES, default="PENDING")
    dt = models.DateTimeField(auto_now_add=True)

class Portfolio(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ptf")
    ast = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="ptf")
    qty = models.IntegerField(default=0)

    class Meta:
        unique_together = ("usr", "ast")
        
class Signal(models.Model):
    ast = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name="sig")
    vol = models.IntegerField()
    rec = models.CharField(max_length=10)
    dt = models.DateTimeField(auto_now=True)