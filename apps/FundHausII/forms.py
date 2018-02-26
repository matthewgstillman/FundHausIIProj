from django import forms

class ProjectForm(forms.Form):
    title = forms.Charfield(label='Project Title')
    founder