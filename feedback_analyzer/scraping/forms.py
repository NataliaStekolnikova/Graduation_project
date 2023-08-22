from django import forms
from .models import ScrapingParams

class ScrapingParamsForm(forms.ModelForm):
    class Meta:
        model = ScrapingParams
        fields = ['param_name', 'param_value']
