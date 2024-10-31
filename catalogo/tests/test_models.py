from django.test import TestCase

# Create your tests here.

from catalogo.models import Autor


class AutorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        Autor.objects.create(nome='João', sobrenome='Silva')

    def test_first_name_label(self):
        autor = Autor.objects.get(id=1)
        field_label = autor._meta.get_field('nome').verbose_name
        self.assertEqual(field_label, 'nome')

    def test_last_name_label(self):
        autor = Autor.objects.get(id=1)
        field_label = autor._meta.get_field('sobrenome').verbose_name
        self.assertEqual(field_label, 'sobrenome')
    
    def test_first_name_max_length(self):
        autor = Autor.objects.get(id=1)
        max_length = autor._meta.get_field('nome').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        autor = Autor.objects.get(id=1)
        max_length = autor._meta.get_field('sobrenome').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        autor = Autor.objects.get(id=1)
        expected_object_name = '{0}, {1}'.format(autor.sobrenome, autor.nome)

        self.assertEqual(str(autor), expected_object_name)

    def test_get_absolute_url(self):
        autor = Autor.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(autor.get_absolute_url(), '/catalogo/autor/1')