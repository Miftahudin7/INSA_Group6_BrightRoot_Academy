from django.urls import path
from .views import (
    GenerateSummaryView, 
    GenerateQuizView, 
    GetUserSummariesView, 
    GetUserQuizzesView,
    SupabaseSignupView,
    SupabaseLoginView,
)

urlpatterns = [
    path('signup/', SupabaseSignupView.as_view(), name='supabase-signup'),
    path('login/', SupabaseLoginView.as_view(), name='supabase-login'),
    path('summary/generate/', GenerateSummaryView.as_view(), name='generate-summary'),
    path('quiz/generate/', GenerateQuizView.as_view(), name='generate-quiz'),
    path('summaries/', GetUserSummariesView.as_view(), name='user-summaries'),
    path('quizzes/', GetUserQuizzesView.as_view(), name='user-quizzes'),
]
