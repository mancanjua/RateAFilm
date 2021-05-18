from django import forms


class UploadFileForm(forms.Form):
    movies = forms.FileField()
    ratings = forms.FileField()

class CreateRating(forms.Form):
    LISTA = (("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"))
    rating = forms.ChoiceField(label="Select the rating", choices=LISTA)
