from django.urls import path
from .views import BackupFileList,DeleteBackupFile,CreateBackup

urlpatterns = [
    path('filelist/',BackupFileList.as_view()),
    path('filedelete/<int:pk>',DeleteBackupFile.as_view()),
    path('createbackup/',CreateBackup.as_view())
]