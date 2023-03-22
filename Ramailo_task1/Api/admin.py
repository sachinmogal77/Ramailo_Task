from django.contrib import admin
from .models import SalesInvoice,BackupFile
# Register your models here.

@admin.register(SalesInvoice)
class SalesInvoiceAdmin(admin.ModelAdmin):
    list_display=['customer_name','phone','address','amount','discount_amount','tax_percent','invoice_items']

@admin.register(BackupFile)
class BackupFileAdmin(admin.ModelAdmin):
    list_display=['file','backup_date','num_rows','size_of_file','file_type']