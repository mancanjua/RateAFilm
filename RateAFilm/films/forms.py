from django import forms


class UploadFileForm(forms.Form):
    movies = forms.FileField()
    ratings = forms.FileField()
