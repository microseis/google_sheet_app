from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('ord_id', 'ord_num', 'ord_cost', 'ord_cost_rub', 'ord_date')
