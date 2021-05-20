from django import forms


class UploadFileForm(forms.Form):
    movies = forms.FileField()
    ratings = forms.FileField()

class CreateRating(forms.Form):
    LISTA = (("1", "1"), ("1.5", "1.5"), ("2", "2"), ("2.5", "2.5"), ("3", "3"), ("3.5", "3.5"), ("4", "4"),
             ("4.5", "4.5"), ("5", "5"))
    rating = forms.ChoiceField(label="Select the rating", choices=LISTA)
