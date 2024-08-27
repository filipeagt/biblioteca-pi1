from django.test import TestCase

import datetime
from catalogo.forms import RenewBookForm


class RenewBookFormTest(TestCase):

    def test_renew_form_date_in_past(self):
        """Teste de formulário é inválido se a data de renovação estiver no passado."""
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        """Teste de formulário é inválido se a data de renovaão estiver a mais de 4 semanas no futuro."""
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        """Teste de formulário é válido se a data de renovação for hoje"""
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        """Teste de formulário é válido se a data de renovação estiver dentro de 4 semanas."""
        date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_field_label(self):
        """Testa se o label de renewal_date é 'Data de renovação'."""
        form = RenewBookForm()
        self.assertTrue(
            form.fields['renewal_date'].label is None or
            form.fields['renewal_date'].label == 'Data de renovação')

    def test_renew_form_date_field_help_text(self):
        """Testa se o texto de ajuda está correto."""
        form = RenewBookForm()
        self.assertEqual(
            form.fields['renewal_date'].help_text,
            'Insira uma data entra agora e 4 semanas (padrão 3).')
