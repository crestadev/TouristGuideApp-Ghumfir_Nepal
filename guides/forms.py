from django import forms
from .models import ItineraryItem

class ItineraryItemForm(forms.ModelForm):
    class Meta:
        model = ItineraryItem
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }
