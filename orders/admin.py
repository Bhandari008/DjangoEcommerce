from django.urls import reverse
from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe
# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')

def order_pdf(obj):
    url = reverse('orders:admin_order_pdf',args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = "Invoice"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','address','state','district','paid','created','updated',order_detail,order_pdf]
    list_filter = ['paid','created','updated']
    inlines = [OrderItemInline]



