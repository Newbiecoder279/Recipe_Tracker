from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . models import CreateUser,NewRecipe
class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']
        
class AddPP(forms.ModelForm):
     class Meta:
         model = CreateUser
         fields = ['profile_pic']


class NewRecipeForm(forms.ModelForm):
    class Meta:
        model = NewRecipe
        fields = ['title','picture', 'ingrediants','instructions']
        
        


