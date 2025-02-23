from .models import Book, Autor, BookInstance, Gênero
from rest_framework import serializers


class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        depth = 1

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'
        depth = 0

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gênero
        fields = '__all__'
        depth = 0

class ExemplarSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = ['id', 'due_back', 'status', 'book']
        depth = 2
