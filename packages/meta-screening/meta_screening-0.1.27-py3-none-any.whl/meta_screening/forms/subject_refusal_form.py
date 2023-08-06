from django import forms
from django.urls.base import reverse
from django.utils.safestring import mark_safe
from edc_dashboard.url_names import url_names
from edc_form_validators import FormValidatorMixin

from ..form_validators import SubjectRefusalFormValidator
from ..models import SubjectRefusal


class ConsentedFormMixin:
    def clean(self):
        cleaned_data = super().clean()
        if self.instance.id:
            url_name = url_names.get("screening_listboard_url")
            url = reverse(
                url_name,
                kwargs={"screening_identifier": self.instance.screening_identifier},
            )
            msg = mark_safe(
                "This form is not relevant. Subject has already consented. "
                f'See subject <A href="{url}?q={self.instance.screening_identifier}">'
                f"{self.instance.screening_identifier}</A>"
            )
            raise forms.ValidationError(msg)
        return cleaned_data


class SubjectRefusalForm(ConsentedFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = SubjectRefusalFormValidator

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = SubjectRefusal
        fields = "__all__"
