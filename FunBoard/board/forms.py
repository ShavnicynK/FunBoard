from django import forms
from .models import Category, Advertisement, Reaction, News
from froala_editor.widgets import FroalaEditor


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = [
            'name',
        ]

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Название категории'
        self.fields['name'].widget.attrs['maxlenght'] = '120'
        self.fields['name'].label = ''
        self.fields['name'].help_text = '<span class="form-text text-muted"><small>Максимальная длина 120 символов</small></span>'


class AdvertisementForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = [
            'name',
            'content',
            'category',
        ]

        widgets = {
            'content': FroalaEditor(),
        }


class ReactionForm(forms.ModelForm):

    class Meta:
        model = Reaction
        fields = [
            'content',

        ]


class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = [
            'name',
            'content',
        ]

        widgets = {
            'content': FroalaEditor(),
        }
