from django import forms

class document_form(forms.Form):
    name = forms.CharField(required=True)
    description = forms.CharField(required=False)
    #image = forms.FileField(required=False)