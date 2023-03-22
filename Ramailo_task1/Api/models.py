from django.db import models
from django.utils import timezone

# Create your models here.
class SalesInvoice(models.Model):
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2)
    invoice_items = models.JSONField()

#     from datetime import datetime
# dummy_data = [    {        
#                        'customer_name': 'John Doe',    
#                        'phone': '1234567890',        
#                        'address': '123 Main St, Anytown USA',        
#                        'amount': 100.00,        
#                        'discount_amount': 10.00,        
#                        'tax_percent': 7.5,        
#                        'invoice_items': [            
#                             {'product_name': 'Widget A','rate': 5.00,  'quantity': 10,'unit': 'each'},            
#                             {'product_name': 'Widget B','rate': 7.50,   'quantity': 5, 'unit': 'each'},  
#                          ]
#     }
# ]
# for data in dummy_data:
#     invoice = SalesInvoice(**data)
#     invoice.save()


    

# invoice1 = SalesInvoice.objects.create(
#     customer_name='John Doe',
#     phone='1234567890',
#     address='123 Main St, Anytown USA',
#     amount=100.00,
#     discount_amount=10.00,
#     tax_percent=5.00,
#     invoice_items=[
#         {'product_name': 'Widget A', 'rate': 1.00, 'quantity': 50, 'unit': 'pcs'},
#         {'product_name': 'Widget B', 'rate': 2.00, 'quantity': 25, 'unit': 'pcs'},
#     ],
#     created_at=timezone.now(),
# )

# invoice2 = SalesInvoice.objects.create(
#     customer_name='Jane Doe',
#     phone='0987654321',
#     address='456 Elm St, Anytown USA',
#     amount=200.00,
#     discount_amount=20.00,
#     tax_percent=10.00,
#     invoice_items=[
#         {'product_name': 'Widget C', 'rate': 3.00, 'quantity': 10, 'unit': 'pcs'},
#         {'product_name': 'Widget D', 'rate': 4.00, 'quantity': 20, 'unit': 'pcs'},
#     ],
#     created_at=timezone.now(),
# )


class BackupFile(models.Model):
    FILE_TYPE_CHOICES = (
        ('csv','CSV'),
        ('xlsx','Excel'),
        ('json','JSON'),
    )

    file = models.FileField(upload_to='backups/')
    backup_date = models.DateField(auto_now_add=True)
    num_rows = models.IntegerField()
    size_of_file = models.CharField(max_length=30)
    file_type = models.CharField(max_length=10,choices=FILE_TYPE_CHOICES)

    def __str__(self):
        return f'{self.file_type} file created on {self.backup_date}'
