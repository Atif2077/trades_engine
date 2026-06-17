from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Asset, Wallet, Order, Portfolio
from .serializers import AssetSerializer, WalletSerializer, OrderSerializer, PortfolioSerializer

class AssetListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        asts = Asset.objects.all()
        sz = AssetSerializer(asts, many=True)
        return Response(sz.data, status=status.HTTP_200_OK)

class WalletAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wlt, _ = Wallet.objects.get_or_create(usr=request.user)
        sz = WalletSerializer(wlt)
        return Response(sz.data, status=status.HTTP_200_OK)

class PortfolioAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ptf = Portfolio.objects.filter(usr=request.user).select_related("ast")
        sz = PortfolioSerializer(ptf, many=True)
        return Response(sz.data, status=status.HTTP_200_OK)

class OrderAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ords = Order.objects.filter(usr=request.user).order_by("-dt")
        sz = OrderSerializer(ords, many=True)
        return Response(sz.data, status=status.HTTP_200_OK)

    def post(self, request):
        sz = OrderSerializer(data=request.data)
        if not sz.is_valid():
            return Response(sz.errors, status=status.HTTP_400_BAD_REQUEST)

        ast_id = sz.validated_data["ast"].id
        qty = sz.validated_data["qty"]
        act = sz.validated_data["act"]
        typ = sz.validated_data.get("typ", "MARKET")

        if qty <= 0:
            return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                ast = Asset.objects.select_for_update().get(id=ast_id)
                wlt, _ = Wallet.objects.select_for_update().get_or_create(usr=request.user)
                tot_cst = ast.prc * qty

                ord_obj = Order.objects.create(
                    usr=request.user,
                    ast=ast,
                    typ=typ,
                    act=act,
                    qty=qty,
                    lmt_prc=sz.validated_data.get("lmt_prc")
                )

                if act == "BUY":
                    if wlt.bal < tot_cst:
                        ord_obj.st = "FAILED"
                        ord_obj.save()
                        return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
                    
                    wlt.bal -= tot_cst
                    wlt.save()

                    ptf, _ = Portfolio.objects.select_for_update().get_or_create(usr=request.user, ast=ast)
                    ptf.qty += qty
                    ptf.save()

                elif act == "SELL":
                    try:
                        ptf = Portfolio.objects.select_for_update().get(usr=request.user, ast=ast)
                        if ptf.qty < qty:
                            raise Portfolio.DoesNotExist
                    except Portfolio.DoesNotExist:
                        ord_obj.st = "FAILED"
                        ord_obj.save()
                        return Response({"error": "Insufficient asset"}, status=status.HTTP_400_BAD_REQUEST)

                    ptf.qty -= qty
                    if ptf.qty == 0:
                        ptf.delete()
                    else:
                        ptf.save()

                    wlt.bal += tot_cst
                    wlt.save()

                ord_obj.st = "FILLED"
                ord_obj.save()
                return Response(OrderSerializer(ord_obj).data, status=status.HTTP_201_CREATED)

        except Exception:
            return Response({"error": "Transaction failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)