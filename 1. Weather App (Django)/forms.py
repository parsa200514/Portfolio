"""
Definition of forms.
"""

from django import forms

class Location_Input(forms.Form):
    location = forms.CharField(max_length=10, label='Location ', required=True, widget=forms.TextInput(attrs={'id': 'id_location'}))
