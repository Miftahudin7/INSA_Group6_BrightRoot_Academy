from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from supabase import create_client
from core.supabase_client import supabase as supabase_client_singleton
from .models import UploadedFile, CommonBook
from .serializers import UploadedFileSerializer, CommonBookSerializer
import re
import os
from io import BytesIO
import tempfile
import requests
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404, HttpResponse


USE_DUMMY_UPLOAD = os.getenv("USE_DUMMY_UPLOAD", "0") == "1"

class FileUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        uploaded_file = request.FILES.get('file')
        title = request.data.get('title')
        description = request.data.get('description', '')
        subject = request.data.get('subject')
        grade = request.data.get('grade')

        if not uploaded_file or not title or not subject or not grade:
            return Response(
                {'error': 'File, title, subject, and grade are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate subject/grade choices
        if subject not in dict(UploadedFile._meta.get_field('subject').choices):
            return Response({'error': 'Invalid subject.'}, status=status.HTTP_400_BAD_REQUEST)
        if grade not in dict(UploadedFile._meta.get_field('grade').choices):
            return Response({'error': 'Invalid grade.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if USE_DUMMY_UPLOAD:
                # ✅ Dummy file URL (testing only)
                file_url = "https://example.com/dummy-file.pdf"
            else:
                # ✅ Real Supabase upload
                supabase_client = supabase_client_singleton
                bucket_name = "uploads"

                # Sanitize path parts
                def sanitize(segment: str) -> str:
                    return re.sub(r"[^A-Za-z0-9._-]", "-", segment.strip())

                safe_user = sanitize(request.user.username)
                safe_grade = sanitize(grade)
                safe_subject = sanitize(subject)
                safe_filename = sanitize(uploaded_file.name)

                file_path = f"{safe_user}/{safe_grade}/{safe_subject}/{safe_filename}"

                # Ensure bucket exists (idempotent)
                # try:
                #     supabase_client.storage.create_bucket(bucket_name, public=True)
                # except Exception as e:
                #     if 'Bucket already exists' not in str(e):
                #         return Response({'error': f'Bucket error: {str(e)}'}, status=500)

                # Upload file to Supabase
                try:
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        for chunk in uploaded_file.chunks():
                            tmp_file.write(chunk)
                        tmp_file_path = tmp_file.name

                    res = supabase_client.storage.from_(bucket_name).upload(
                        file_path,
                        tmp_file_path
                    )

                    if isinstance(res, dict) and res.get("error"):
                        return Response({'error': res["error"]["message"]}, status=500)
                
                finally:
                    if os.path.exists(tmp_file_path):
                        os.remove(tmp_file_path)

                # Get public URL
                file_url = supabase_client.storage.from_(bucket_name).get_public_url(file_path)
                

            # Save metadata in DB
            file_record = UploadedFile.objects.create(
                user=request.user,
                title=title,
                description=description,
                subject=subject,
                grade=grade,
                file_name=uploaded_file.name,
                file_url=file_url
            )

            serializer = UploadedFileSerializer(file_record)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': f"Server error when saving file: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def download_file(request, file_id):
    file_obj = get_object_or_404(UploadedFile, id=file_id)
    if not file_obj.file_url:
        raise Http404("File URL not set")

    # Download the file from Supabase
    r = requests.get(file_obj.file_url, stream=True)
    if r.status_code != 200:
        raise Http404("File not found on storage")

    response = HttpResponse(
        r.raw,
        content_type=r.headers.get("content-type", "application/octet-stream")
    )
    response['Content-Disposition'] = f'attachment; filename="{file_obj.file_name}"'
    return response

class GetUserFilesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        files = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at')
        serializer = UploadedFileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetCommonBooksView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        subject = request.query_params.get('subject')
        grade = request.query_params.get('grade')
        
        books = CommonBook.objects.filter(is_active=True)
        
        if subject:
            books = books.filter(subject=subject)
        if grade:
            books = books.filter(grade=grade)
            
        serializer = CommonBookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
