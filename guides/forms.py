from django import forms
from .models import ItineraryItem, Review

# -------------------------------
# Review Form
# -------------------------------
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            # Use a select dropdown for rating (1–5 stars)
            'rating': forms.Select(
                choices=[(i, f'{i} Stars') for i in range(1, 6)],
                attrs={'class': 'form-select'}
            ),
            # Textarea for comments with placeholder
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Write your review...'
                }
            ),
        }

# -------------------------------
# Itinerary Item Form (with validation)
# -------------------------------
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

    # Optional: Add validation to ensure start_date <= end_date
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Start date cannot be after end date.")
