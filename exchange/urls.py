from django.urls import path
from . import views
from . import api

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("order/execute/", views.execute_order, name="execute_order"),
    path("wallet/fund/", views.add_funds, name="add_funds"),
    path("api/v1/assets/", api.AssetListAPI.as_view(), name="api_assets"),
    path("api/v1/wallet/", api.WalletAPI.as_view(), name="api_wallet"),
    path("api/v1/portfolio/", api.PortfolioAPI.as_view(), name="api_portfolio"),
    path("api/v1/orders/", api.OrderAPI.as_view(), name="api_orders"),
]