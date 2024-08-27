from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime  # para verificar o intervalo de datas de renovação.

from django import forms


class RenewBookForm(forms.Form):
    """Formulário para a renovação de livros."""
    renewal_date = forms.DateField(
            help_text="Insira uma data entra agora e 4 semanas (padrão 3).", label='Data de renovação')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Verifica se a data não está no passado.
        if data < datetime.date.today():
            raise ValidationError(_('Data Inválida - renovação no passado'))
        # Verifica se a data está no intervalo vaĺido
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Data Inválida - renovação com mais de 4 semanas'))

        return data
