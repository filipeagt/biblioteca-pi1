from django.db import models

from django.urls import reverse  


class Gênero(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Insira um gênero (Ex. Ficção Científica, Infantil etc.)",
        verbose_name='Nome'
    )

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('gênero-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    título = models.CharField(max_length=200)
    autor = models.ForeignKey('Autor', on_delete=models.RESTRICT, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books.
    # Author as a string rather than object because it hasn't been declared yet in file.
    resumo = models.TextField(
        max_length=1000, help_text="Insira uma breve descrição do livro.")
    #isbn = models.CharField('ISBN', max_length=13,
     #                       unique=True,
      #                      help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
       #                               '">ISBN number</a>')
    gênero = models.ManyToManyField(
        Gênero, help_text="Selecione um gênero para este livro")
    # ManyToManyField used because a genre can contain many books and a Book can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    #language = models.ForeignKey(
     #   'Language', on_delete=models.SET_NULL, null=True)

    idade = models.PositiveSmallIntegerField('Faixa etária', default=0)

    capa = models.TextField(max_length=1000, help_text="Insira um link para a imagem da capa do livro.", default="https://vectorportal.com/storage/book-vector(1).jpg")

    class Meta:
        ordering = ['título', 'autor']

    def display_gênero(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([gênero.name for gênero in self.gênero.all()[:3]])

    display_gênero.short_description = 'Gênero'

    def get_absolute_url(self):
        """Returns the url to access a particular book record."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.título


import uuid  # Required for unique book instances
from datetime import date

from django.conf import settings  # Required to assign User as a borrower


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Identificação única para o livro no sistema")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True, verbose_name='Livro')
    #imprint = models.CharField(max_length=200)
    due_back = models.DateField('Devolução', null=True, blank=True, help_text='Data de devolução')
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Mutuário')

    @property
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)

    LOAN_STATUS = (
        #('d', 'Maintenance'),
        ('o', 'Emprestado'),
        ('a', 'Disponível'),
        #('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Disponibilidade do livro')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('bookinstance-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.título})'


class Autor(models.Model):
    """Model representing an author."""
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    #date_of_birth = models.DateField(null=True, blank=True)
    #date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['sobrenome', 'nome']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('autor-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.sobrenome}, {self.nome}'
