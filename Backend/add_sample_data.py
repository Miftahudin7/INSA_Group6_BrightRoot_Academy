#!/usr/bin/env python
"""
Script to add sample common books to the database
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from notes.models import CommonBook

def add_sample_books():
    """Add sample common books to the database"""
    
    # Sample books data
    sample_books = [
        {
            'title': 'Algebra Fundamentals - Grade 9',
            'subject': 'Math',
            'grade': 'Grade9',
            'description': 'Comprehensive guide to algebra basics for 9th grade students',
            'file_url': 'https://example.com/algebra_grade9.pdf'
        },
        {
            'title': 'English Literature Classics - Grade 10',
            'subject': 'English',
            'grade': 'Grade10',
            'description': 'Collection of classic literature works for 10th grade',
            'file_url': 'https://example.com/english_lit_grade10.pdf'
        },
        {
            'title': 'Physics Principles - Grade 11',
            'subject': 'Science',
            'grade': 'Grade11',
            'description': 'Introduction to physics concepts for 11th grade',
            'file_url': 'https://example.com/physics_grade11.pdf'
        },
        {
            'title': 'World History - Grade 12',
            'subject': 'History',
            'grade': 'Grade12',
            'description': 'Comprehensive world history for 12th grade',
            'file_url': 'https://example.com/history_grade12.pdf'
        },
        {
            'title': 'Computer Science Basics - Grade 9',
            'subject': 'Computer',
            'grade': 'Grade9',
            'description': 'Introduction to computer science for beginners',
            'file_url': 'https://example.com/cs_grade9.pdf'
        }
    ]
    
    # Add books to database
    for book_data in sample_books:
        book, created = CommonBook.objects.get_or_create(
            title=book_data['title'],
            defaults=book_data
        )
        if created:
            print(f"Created: {book.title}")
        else:
            print(f"Already exists: {book.title}")
    
    print("\nSample books added successfully!")

if __name__ == '__main__':
    add_sample_books()
