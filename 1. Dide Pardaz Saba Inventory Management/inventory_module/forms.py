from django import forms
from .models import Device
from .models import Brand


class BrandSelectionForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), label="Select Brand")


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['brand', 'model', 'color', 'price', 'display_size', 'in_stock']
