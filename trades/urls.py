from django.contrib import admin
from django.urls import path, include
from exchange.views import DashboardView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("exchange.urls")),
    path("ai-signals/", DashboardView.as_view(), name="ai_dashboard"),
]