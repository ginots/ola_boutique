from django.utils import timezone
from datetime import timedelta
from client_app.models import TableOrders

def notifications(request):
    today = timezone.localdate()

    reminders = []

    # 🔔 3 days before delivery
    upcoming = TableOrders.objects.filter(
        due_date=today + timedelta(days=3),
        status="Ordered"
    )

    for order in upcoming:
        reminders.append(
            f"🧵 Order #{order.order_id} is due in 3 days"
        )

    # ⚠️ Missed deliveries (1 day after)
    missed = TableOrders.objects.filter(
        due_date=today - timedelta(days=1),
        status="Ordered"
    )

    for order in missed:
        reminders.append(
            f"⚠ Order #{order.order_id} was missed yesterday"
        )

    return {
        "notifications": reminders,
        "notification_count": len(reminders)
    }

from django.db import models
from .models import TableStock

def low_stock_messages(request):
    low_items = TableStock.objects.filter(
        stock__lte=models.F("low_stock")
    )

    messages = []
    for item in low_items:
        messages.append({
            "item": item.item,
            "stock": item.stock,
            "unit": item.unit
        })

    return {
        "low_stock_messages": messages,
        "low_stock_count": len(messages)
    }
