from celery import shared_task
from .models import Asset
from .utils import generate_ai_signal

@shared_task
def update_all_ai_signals():
    asts = Asset.objects.all()
    for ast in asts:
        generate_ai_signal(ast.tkr)