from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime  # for checking renewal date range.

from django import forms


class RenewBookForm(forms.Form):
    """Form for a librarian to renew books."""
    renewal_date = forms.DateField(
            help_text="Insira uma data entra agora e 4 semanas (padrão 3).", label='Data de renovação')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Data Inválida - renovação no passado'))
        # Check date is in range librarian allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Data Inválida - renovação com mais de 4 semanas'))

        # Remember to always return the cleaned data.
        return data
