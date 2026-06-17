from rest_framework import serializers
from .models import Asset, Wallet, Order, Portfolio

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["usr", "st"]

class PortfolioSerializer(serializers.ModelSerializer):
    tkr = serializers.CharField(source="ast.tkr", read_only=True)
    name = serializers.CharField(source="ast.name", read_only=True)
    cur_prc = serializers.DecimalField(source="ast.prc", max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Portfolio
        fields = ["id", "ast", "tkr", "name", "qty", "cur_prc"]