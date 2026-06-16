from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("order/execute/", views.execute_order, name="execute_order"),
    path("wallet/fund/", views.add_funds, name="add_funds"),
]