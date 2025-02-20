from .models import Book, Autor, BookInstance, Gênero, Language
from rest_framework import serializers


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['título', 'nome', 'capa']
