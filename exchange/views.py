from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Asset, Wallet, Order, Portfolio
from .utils import sync_market_prices
from decimal import Decimal


@login_required
def dashboard(request):
    sync_market_prices()
    
    wlt, _ = Wallet.objects.get_or_create(usr=request.user)
    asts = Asset.objects.all()
    ptf = Portfolio.objects.filter(usr=request.user).select_related("ast")
    ords = Order.objects.filter(usr=request.user).order_by("-dt")[:10]
    
    ctx = {
        "wlt": wlt,
        "asts": asts,
        "ptf": ptf,
        "ords": ords,
    }
    return render(request, "exchange/dashboard.html", ctx)

@login_required
def execute_order(request):
    if request.method != "POST":
        return redirect("dashboard")
        
    ast_id = request.POST.get("ast_id")
    qty_str = request.POST.get("qty")
    act = request.POST.get("act")
    typ = request.POST.get("typ", "MARKET")
    
    if not all([ast_id, qty_str, act]):
        messages.error(request, "Missing required parameters")
        return redirect("dashboard")
        
    try:
        qty = int(qty_str)
        if qty <= 0:
            messages.error(request, "Quantity must be greater than zero")
            return redirect("dashboard")
    except ValueError:
        messages.error(request, "Invalid quantity format")
        return redirect("dashboard")
        
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
            )
            
            if act == "BUY":
                if wlt.bal < tot_cst:
                    ord_obj.st = "FAILED"
                    ord_obj.save()
                    messages.error(request, "Insufficient wallet balance")
                    return redirect("dashboard")
                    
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
                    messages.error(request, "Insufficient portfolio assets")
                    return redirect("dashboard")
                    
                ptf.qty -= qty
                if ptf.qty == 0:
                    ptf.delete()
                else:
                    ptf.save()
                    
                wlt.bal += tot_cst
                wlt.save()
                
            ord_obj.st = "FILLED"
            ord_obj.save()
            messages.success(request, f"Order {act} executed successfully")
            
    except Exception:
        messages.error(request, "Transaction failed due to an unexpected error")
        
    return redirect("dashboard")

@login_required
def add_funds(request):
    if request.method != "POST":
        return redirect("dashboard")
        
    amt_str = request.POST.get("amount")
    
    try:
        amt = Decimal(amt_str)
        if amt <= 0:
            messages.error(request, "Deposit amount must be greater than zero")
            return redirect("dashboard")
            
        with transaction.atomic():
            wlt, _ = Wallet.objects.select_for_update().get_or_create(usr=request.user)
            wlt.bal += amt
            wlt.save()
            
        messages.success(request, f"Successfully deposited ${amt} into your wallet")
    except Exception:
        messages.error(request, "Invalid amount provided")
        
    return redirect("dashboard")