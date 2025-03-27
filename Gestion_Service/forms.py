from django import forms
from .models import DemandeService

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = DemandeService
        fields = ['description', 'fichier']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez votre demande en détail...'
            }),
            'fichier': forms.FileInput(attrs={
                'class': 'form-control',
                
            })
        }