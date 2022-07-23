from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
import datetime
from orders.models import Order


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0,microsecond=0)
        today_end = now.replace(hour=23, minute=59,second=59, microsecond=999999)-datetime.timedelta(days=2)
        qs = Order.objects.filter(timestamp__gte=today_start,timestamp__lte=today_end, status="created")
        qs.update(status="stale")