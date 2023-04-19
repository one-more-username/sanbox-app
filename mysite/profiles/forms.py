from django import forms
# class LocationForm(forms.Form):
#     birthdate = forms.CharField(label='birthdate')
#     gender = forms.CharField(label='gender')
#     photos = forms.ImageField(
#         label='photos',
#         widget=forms.FileInput(attrs={'multiple': 'multiple'})
#     )

from django import forms
from .models import Profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'user',
            'birthdate',
            'gender',
            'image',
            'images',
        ]
        widgets = {
            'user': forms.TextInput(attrs={'placeholder': 'User', 'class': 'form-control'}),
            'birthdate': forms.DateField(attrs={'placeholder': 'Birth date', 'class': 'form-control'}),
            'gender': forms.Textarea(attrs={'placeholder': 'Gender', 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'images': forms.FileInput(attrs={'class': 'form-control', 'multiple': 'multiple'}),
        }
        labels = {
            'user': 'User',
            'birthdate': 'Birth date',
            'gender': 'Gender',
            'image': 'Main image',
            'images': 'Other images',
        }
