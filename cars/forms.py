from django import forms
from .models import Category

class SearchForm(forms.Form):
    search_query = forms.CharField(
        label='Pesquisar',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Digite marca, modelo...'})
    )
    min_price = forms.DecimalField(
        label='Preço mínimo',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'R$ mínimo'})
    )
    max_price = forms.DecimalField(
        label='Preço máximo',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'R$ máximo'})
    )
    category = forms.ModelChoiceField(
        label='Categoria',
        required=False,
        queryset=Category.objects.all(),
        empty_label='Todas categorias'
    )



