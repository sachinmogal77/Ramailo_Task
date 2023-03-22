from django.shortcuts import render
from datetime import datetime
import csv
import io
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SalesInvoice, BackupFile
# Create your views here.
import csv
import json
from datetime import datetime

from rest_framework.views import APIView
# from django.core.exceptions import ObjectDoesNotExist
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
# from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.response import Response
from .models import SalesInvoice, BackupFile
from .serializers import BackupFileSerializer,SalesInvoiceSerializer
from rest_framework import viewsets
import openpyxl

class SalesInvoiceAPI(viewsets.ModelViewSet):
    querysets = SalesInvoice.objects.all()
    serializer_class =SalesInvoiceSerializer

class BackupFileList(generics.ListAPIView):
    queryset = BackupFile.objects.all()
    serializer_class = BackupFileSerializer

class DeleteBackupFile(APIView):
    def delete(self,request,backup_file_id):
        try:
            backup_file=BackupFile.objects.get(id=backup_file_id)
            backup_file.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BackupFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# class BackupFileDelete(generics.DestroyAPIView):
#     queryset = BackupFile.objects.all()
#     serializer_class = BackupFileSerializer

class CreateBackup(APIView):
    def post(self, request):
        # Get user input for file type and date range
        file_type = request.data.get('file_type', '').lower()
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        # Validate user input
        if file_type not in ['csv', 'excel', 'json']:
            return Response({'error': 'Invalid file type'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if backup file already exists
        backup_file_name = f"{start_date.strftime('%Y%m%d')}salesinvoice{end_date.strftime('%Y%m%d')}.{file_type}"
        if BackupFile.objects.filter(file__icontains=backup_file_name).exists():
            return Response({'error': f"{backup_file_name} already exists"}, status=status.HTTP_400_BAD_REQUEST)


        # invoices = SalesInvoice.objects.filter(created_at__range=[start_date, end_date])
         # Get all invoices within the date range
        invoices = SalesInvoice.objects.filter(created_at__range=(start_date, end_date))
        num_rows = invoices.count()

        # Serialize invoices to the appropriate file format
        if file_type == 'csv':
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['id', 'customer_name', 'phone', 'address', 'amount', 'discount_amount', 'tax_percent', 'invoice_items'])
            for invoice in invoices:
                writer.writerow([invoice.id, invoice.customer_name, invoice.phone, invoice.address, invoice.amount, invoice.discount_amount, invoice.tax_percent, invoice.invoice_items])
            file_content = output.getvalue()
            file_extension = 'csv'
        elif file_type == 'excel':
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(['id', 'customer_name', 'phone', 'address', 'amount', 'discount_amount', 'tax_percent', 'invoice_items'])
            for invoice in invoices:
                ws.append([invoice.id, invoice.customer_name, invoice.phone, invoice.address, invoice.amount, invoice.discount_amount, invoice.tax_percent, invoice.invoice_items])
        # elif file_type == 'excel':
        #     pass
        # elif file_type == 'json':
        #     pass
            output = io.BytesIO()
            wb.save(output)
            file_content = output.getvalue()
            file_extension = 'xlsx'
        elif file_type == 'json':
            invoices_list = []
            for invoice in invoices:
                invoice_dict = {
                    'id': invoice.id,
                    'customer_name': invoice.customer_name,
                    'phone': invoice.phone,
                    'address': invoice.address,
                    'amount': invoice.amount,
                    'discount_amount': invoice.discount_amount,
                    'tax_percent': invoice.tax_percent,
                    'invoice_items': invoice.invoice_items,
                }
                invoices_list.append(invoice_dict)
            file_content = json.dumps(invoices_list, indent=4)
            file_extension = 'json'

        # Save backup file to disk and create BackupFile instance
        backup_file = BackupFile()
        backup_file.file.save(backup_file_name, file_content)
        backup_file.num_rows = num_rows
        backup_file.file_size = f"{len(file_content)} bytes"
        backup_file.file_type = file_extension
        backup_file.save()

        # Return success response with BackupFile instance
        serializer = BackupFileSerializer(backup_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


































































# class SalesInvoiceBackup(generics.GenericAPIView):
#     queryset = SalesInvoice.objects.all()

#     @csrf_exempt
#     def post(self, request, format=None):
#         file_type = request.POST.get('file_type')
#         start_date_str = request.POST.get('start_date')
#         end_date_str = request.POST.get('end_date')
#         try:
#             start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
#             end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
#         except (ValueError, TypeError):
#             return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
#         if start_date > end_date:
#             return Response({'error': 'Start date cannot be greater than end date.'}, status=status.HTTP_400_BAD_REQUEST)

#         backup_filename = f"{start_date.strftime('%Y%m%d')}salesinvoice{end_date.strftime('%Y%m%d')}.{file_type}"
#         try:
#             existing_file = BackupFile.objects.get(file_type=file_type, backup_date=start_date)
#             return Response({'error': f"{existing_file} already exists."}, status=status.HTTP_400_BAD_REQUEST)
#         except ObjectDoesNotExist:
#             pass

#         invoices = SalesInvoice.objects.filter(backup_date__range=(start_date, end_date))
