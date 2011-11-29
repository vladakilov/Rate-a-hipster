from django import forms

class document_form(forms.Form):
    name = forms.CharField(required=True, error_messages={'required': 'Please enter a valid name'})
    description = forms.CharField(required=False)
    #image = forms.FileField(required=False)