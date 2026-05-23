from django import forms
from .models import Sertifikat

class SertifikatForm(forms.ModelForm):
    class Meta:
        model = Sertifikat
        fields = ['fio', 'kurs', 'nomi', 'tashkilot', 'link', 'berilgan']
        widgets = {
            'fio':       forms.TextInput(attrs={'placeholder': 'Familiya Ism Sharif'}),
            'nomi':      forms.TextInput(attrs={'placeholder': 'Sertifikat nomini kiriting'}),
            'tashkilot': forms.TextInput(attrs={'placeholder': 'Masalan: Coursera, Google, IT-Park'}),
            'link':      forms.URLInput(attrs={'placeholder': 'https://...'}),
            'kurs':      forms.TextInput(attrs={'placeholder': 'Masalan: 2-kurs'}),
            'berilgan':  forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'fio':       "To'liq F.I.O.",
            'kurs':      "Kurs (talabalar uchun)",
            'nomi':      "Sertifikat nomi",
            'tashkilot': "Bergan tashkilot",
            'link':      "Sertifikat linki",
            'berilgan':  "Berilgan sana",
        }
