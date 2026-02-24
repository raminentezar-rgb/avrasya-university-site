from django import forms
from django.utils.translation import gettext_lazy as _
from .models import News, Announcement, Category


class NewsSearchForm(forms.Form):
    """Haber arama formu"""
    q = forms.CharField(
        label=_('Arama'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Haber ara...')
        })
    )
    
    news_type = forms.ChoiceField(
        label=_('Tür'),
        choices=[('', _('Tümü'))] + News.NEWS_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    category = forms.ModelChoiceField(
        label=_('Kategori'),
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label=_('Tüm Kategoriler'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class QuickAnnouncementForm(forms.ModelForm):
    """Hızlı duyuru formu"""
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'summary', 'image', 'external_link', 'external_link_text', 'announcement_date', 'is_important', 'is_active']
        widgets = {
            'announcement_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'external_link': forms.URLInput(attrs={'class': 'form-control'}),
            'external_link_text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }