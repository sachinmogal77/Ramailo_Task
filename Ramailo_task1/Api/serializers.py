from rest_framework import serializers
from .models import SalesInvoice,BackupFile

class SalesInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInvoice
        fields = '__all__'

class BackupFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupFile
        fields = '__all__'
