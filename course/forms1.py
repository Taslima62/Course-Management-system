from django import forms 
from .models import *
from .models import Profile
 
class ImageForm(forms.ModelForm): 
  
    class Meta: 
        model = Profile 
        fields = [ 'profile_image'] 