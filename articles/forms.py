from django import forms
from pagedown.widgets import AdminPagedownWidget

from articles.models import Article


class ArticleModelForm(forms.ModelForm):
    content = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Article
        fields = '__all__'
