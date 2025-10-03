from django.urls import path
from .views import FileUploadView, GetUserFilesView, GetCommonBooksView, download_file

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/', GetUserFilesView.as_view(), name='user-files'),
    path('common-books/', GetCommonBooksView.as_view(), name='common-books'),
    path('download/<int:file_id>/', download_file, name='download-file'),
]
