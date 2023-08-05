from django import forms
from oscar.forms.widgets import ImageInput

from ..models import DSDProduct


class DSDProductForm(forms.ModelForm):

    class Meta:
        model = DSDProduct
        exclude = []


class DSDPublishProductForm(forms.ModelForm):

    class Meta:
        model = DSDProduct
        fields = ['is_public', ]
