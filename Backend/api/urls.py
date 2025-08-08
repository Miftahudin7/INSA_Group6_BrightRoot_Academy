from django.urls import path
from . import views


urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note_list"),
    path("notr/delete/<int:pk>", views.NoteDelete.as_view(), name="delete-note")

]