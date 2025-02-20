from .models import Book, Autor, BookInstance, Gênero, Language
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['título', 'autor', 'capa']
        depth = 1
