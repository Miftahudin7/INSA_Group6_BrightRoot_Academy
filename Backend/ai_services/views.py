import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import google.generativeai as genai
from core.supabase_client import supabase
from .models import AIRequest
from notes.models import Summary, Quiz, UploadedFile
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyB8zdK48T3Rjniw1aLkCNaYwulaaRdOwB4"
genai.configure(api_key=GEMINI_API_KEY)

class GenerateSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        file_id = request.data.get('file_id')
        if not file_id:
            return Response({'error': 'File ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            file_obj = UploadedFile.objects.get(id=file_id, user=request.user)
            
            # For now, we'll use a placeholder since we need to extract text from the file
            # In production, you'd use a library like PyPDF2 or python-docx to extract text
            file_content = f"Content from {file_obj.title} - {file_obj.subject} for {file_obj.grade}"
            
            # Generate summary using Gemini
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"""
            Please provide a comprehensive summary of the following educational content:
            
            Subject: {file_obj.subject}
            Grade: {file_obj.grade}
            Title: {file_obj.title}
            
            Content: {file_content}
            
            Please provide:
            1. A concise summary (2-3 paragraphs)
            2. Key concepts and main points
            3. Important definitions or formulas
            4. Study recommendations
            
            Format the response in a clear, educational manner suitable for students.
            """
            
            response = model.generate_content(prompt)
            summary_content = response.text
            
            # Save summary to database
            summary = Summary.objects.create(
                user=request.user,
                file=file_obj,
                content=summary_content
            )
            
            # Log AI request
            AIRequest.objects.create(
                user=request.user,
                request_type='summary',
                content=file_content[:500],  # Truncate for storage
                response=summary_content[:500]
            )
            
            return Response({
                'summary': summary_content,
                'summary_id': summary.id,
                'message': 'Summary generated successfully'
            }, status=status.HTTP_200_OK)
            
        except UploadedFile.DoesNotExist:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Failed to generate summary: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SupabaseSignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username') or (email.split('@')[0] if email else None)

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create user in Supabase Auth
            result = supabase.auth.sign_up({
                'email': email,
                'password': password,
                'options': {
                    'data': {'username': username}
                }
            })

            if not result.user:
                return Response({'error': 'Signup failed'}, status=status.HTTP_400_BAD_REQUEST)

            # Immediately confirm the user's email using admin (service role key required)
            try:
                supabase.auth.admin.update_user_by_id(result.user.id, { 'email_confirm': True })
            except Exception:
                # Ignore if admin not permitted; login may require email confirmation in Supabase settings
                pass

            # Ensure a matching Django user exists for DRF auth (use email as username to avoid collisions)
            User = get_user_model()
            django_user = None
            try:
                django_user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            if django_user is None:
                django_user, _ = User.objects.get_or_create(
                    username=email,
                    defaults={'email': email}
                )
            try:
                django_user.set_password(password)
                django_user.save()
            except Exception:
                pass

            # Also sign the user in to return Supabase session and DRF tokens on signup
            session = None
            try:
                session = supabase.auth.sign_in_with_password({'email': email, 'password': password})
            except Exception:
                # If sign-in fails (e.g., confirmation required and admin confirm failed), return 201 without tokens
                return Response({'message': 'Signup successful', 'user': {'id': result.user.id, 'email': result.user.email, 'username': django_user.username}}, status=status.HTTP_201_CREATED)

            # Issue DRF tokens
            refresh = RefreshToken.for_user(django_user)
            access = str(refresh.access_token)

            return Response({
                'message': 'Signup successful',
                'access': access,
                'refresh': str(refresh),
                'supabase_access_token': getattr(session.session, 'access_token', None),
                'supabase_refresh_token': getattr(session.session, 'refresh_token', None),
                'user': {'id': result.user.id, 'email': result.user.email, 'username': django_user.username}
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SupabaseLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = supabase.auth.sign_in_with_password({'email': email, 'password': password})
            if not session.session or not session.session.access_token:
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

            # Pair with a Django user and mint DRF JWTs (email as username)
            User = get_user_model()
            django_user = None
            try:
                django_user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            if django_user is None:
                django_user, _ = User.objects.get_or_create(
                    username=email,
                    defaults={'email': email}
                )

            refresh = RefreshToken.for_user(django_user)
            access = str(refresh.access_token)

            return Response({
                'access': access,
                'refresh': str(refresh),
                'supabase_access_token': session.session.access_token,
                'supabase_refresh_token': session.session.refresh_token,
                'user': {
                    'id': session.user.id,
                    'email': session.user.email,
                    'username': django_user.username,
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            # Surface common Supabase errors helpfully while keeping generic message to client
            msg = str(e)
            if 'Email not confirmed' in msg or 'invalid_credentials' in msg:
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'error': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)

class GenerateQuizView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        file_id = request.data.get('file_id')
        num_questions = request.data.get('num_questions', 5)
        
        if not file_id:
            return Response({'error': 'File ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            file_obj = UploadedFile.objects.get(id=file_id, user=request.user)
            
            # For now, we'll use a placeholder since we need to extract text from the file
            file_content = f"Content from {file_obj.title} - {file_obj.subject} for {file_obj.grade}"
            
            # Generate quiz using Gemini
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"""
            Please create a {num_questions}-question quiz based on the following educational content:
            
            Subject: {file_obj.subject}
            Grade: {file_obj.grade}
            Title: {file_obj.title}
            
            Content: {file_content}
            
            Please provide:
            1. {num_questions} multiple choice questions
            2. 4 answer choices for each question (A, B, C, D)
            3. The correct answer for each question
            4. A brief explanation for each correct answer
            
            Format the response as a JSON object with this structure:
            {{
                "questions": [
                    {{
                        "question": "Question text here?",
                        "options": {{
                            "A": "Option A",
                            "B": "Option B", 
                            "C": "Option C",
                            "D": "Option D"
                        }},
                        "correct_answer": "A",
                        "explanation": "Explanation of why this is correct"
                    }}
                ]
            }}
            
            Make sure the questions are appropriate for the grade level and subject.
            """
            
            response = model.generate_content(prompt)
            quiz_content = response.text
            
            # Try to parse the response as JSON
            try:
                quiz_data = json.loads(quiz_content)
            except json.JSONDecodeError:
                # If parsing fails, create a simple structure
                quiz_data = {
                    "questions": [
                        {
                            "question": "Sample question based on the content?",
                            "options": {
                                "A": "Option A",
                                "B": "Option B",
                                "C": "Option C",
                                "D": "Option D"
                            },
                            "correct_answer": "A",
                            "explanation": "This is a sample explanation"
                        }
                    ]
                }
            
            # Save quiz to database
            quiz = Quiz.objects.create(
                user=request.user,
                file=file_obj,
                questions=quiz_data
            )
            
            # Log AI request
            AIRequest.objects.create(
                user=request.user,
                request_type='quiz',
                content=file_content[:500],
                response=str(quiz_data)[:500]
            )
            
            return Response({
                'quiz': quiz_data,
                'quiz_id': quiz.id,
                'message': 'Quiz generated successfully'
            }, status=status.HTTP_200_OK)
            
        except UploadedFile.DoesNotExist:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Failed to generate quiz: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetUserSummariesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        summaries = Summary.objects.filter(user=request.user).order_by('-created_at')
        data = []
        
        for summary in summaries:
            data.append({
                'id': summary.id,
                'file_title': summary.file.title,
                'subject': summary.file.subject,
                'grade': summary.file.grade,
                'content': summary.content,
                'created_at': summary.created_at
            })
        
        return Response(data, status=status.HTTP_200_OK)

class GetUserQuizzesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        quizzes = Quiz.objects.filter(user=request.user).order_by('-created_at')
        data = []
        
        for quiz in quizzes:
            data.append({
                'id': quiz.id,
                'file_title': quiz.file.title,
                'subject': quiz.file.subject,
                'grade': quiz.file.grade,
                'questions': quiz.questions,
                'created_at': quiz.created_at
            })
        
        return Response(data, status=status.HTTP_200_OK)
