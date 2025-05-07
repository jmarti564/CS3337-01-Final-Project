# 5/4
from django.forms import ModelForm
from .models import Book, Comment

# Form for posting new books
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'price', 'description', 'picture']

# Form for posting comments on books
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
