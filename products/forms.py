from dataclasses import fields
from django import forms
from .models import Product

# class ProductForm(forms.Form):
#     title = forms.CharField()


class ProductForm(forms.ModelForm):
    tags = forms.CharField(label="Related Tags", required=False)

    
    class Meta:
        model = Product
        fields = [
            'title',
            'category',
            'content',
            'image',
            'media',
            'image_size',
            'location',
        ]
        exclude = [ 
            'price',
            'inventory',
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Image Name",
                    "class": "form-control"
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Image Description",
                     "class": "form-control"
                }
            ),
            "category":forms.Select(
                attrs={
                    "placeholder":"Category",
                    "class": 'form-control'
                }
            )
        }
    
    def clean_content(self):
        data = self.cleaned_data.get('content')
        if len(data) < 4:
            raise forms.ValidationError("This is not long enough")
        
        return data