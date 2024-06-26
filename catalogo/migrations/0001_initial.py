# Generated by Django 4.2.11 on 2024-05-16 19:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('sobrenome', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['sobrenome', 'nome'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('título', models.CharField(max_length=200)),
                ('resumo', models.TextField(help_text='Insira uma breve descrição do livro.', max_length=1000)),
                ('idade', models.PositiveSmallIntegerField(default=0, verbose_name='Faixa etária')),
                ('capa', models.TextField(default='https://vectorportal.com/storage/book-vector(1).jpg', help_text='Insira um link para a imagem da capa do livro.', max_length=1000)),
                ('autor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='catalogo.autor')),
            ],
            options={
                'ordering': ['título', 'autor'],
            },
        ),
        migrations.CreateModel(
            name='Gênero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Insira um gênero (Ex. Ficção Científica, Infantil etc.)', max_length=200, unique=True, verbose_name='Nome')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)", max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Identificação única para o livro no sistema', primary_key=True, serialize=False)),
                ('due_back', models.DateField(blank=True, help_text='Data de devolução', null=True, verbose_name='Devolução')),
                ('status', models.CharField(blank=True, choices=[('o', 'Emprestado'), ('a', 'Disponível')], default='a', help_text='Disponibilidade do livro', max_length=1)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='catalogo.book', verbose_name='Livro')),
                ('borrower', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Mutuário')),
            ],
            options={
                'ordering': ['due_back'],
                'permissions': (('can_mark_returned', 'Set book as returned'),),
            },
        ),
        migrations.AddField(
            model_name='book',
            name='gênero',
            field=models.ManyToManyField(help_text='Selecione um gênero para este livro', to='catalogo.gênero'),
        ),
    ]
