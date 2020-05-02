from .models import  City
from django.forms import TextInput,ModelForm

class CityForm(ModelForm):
    class Meta:
        model=City
        fields={'name'}
        widgets={'name':TextInput(attrs={'class':'input','placeholder':'city name'})}
