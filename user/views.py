from django.shortcuts import render,redirect
from django.http import HttpResponse
from . forms import SignupForm, NewRecipeForm, AddPP
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
import requests
from django.contrib.auth.decorators import login_required
from . models import CreateUser, NewRecipe
from django.shortcuts import get_object_or_404
from django.db.models import Q

def home(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    else:
     recipes = []
     for _ in range(6):
        try:
            response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
            data =response.json()
            meal = data.get("meals",[None])[0]
            if meal and meal not in recipes:
                recipes.append(meal)
        except Exception as e:
            print("Error fetching recipe:", e)
            
    return render(request, 'landing.html',{'recipes':recipes})

def user_signup(request):
   if request.method == 'POST':
       form = SignupForm(request.POST)
       profile_form = AddPP(request.POST, request.FILES)
       if form.is_valid() and profile_form.is_valid():
           user = form.save()
           profile = profile_form.save(commit=False)
           profile.user = user
           profile.save()
           login(request, user)
           return redirect('user_login')
           
           
   else:
       form = SignupForm()
       profile_form = AddPP()
       
   return render(request,'includes/signup.html',{'form':form, 'profile_form':profile_form})   

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
            
    else:
        form = AuthenticationForm
    return render(request,'includes/login.html',{'form':form})

def recipe_detail(request, meal_id):
    try:
        url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
        response = requests.get(url)
        data = response.json()
        meal = data.get("meals", [None])[0]
    
    except Exception as e:
        meal = None
        print('Error fetching meals',e)
    
    return render(request,'recipe_detail.html',{'meal':meal})

def user_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='accounts/login/')     
def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('home')
      
    recipes = []
    for _ in range(6):
        try:
            response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
            data =response.json()
            meal = data.get("meals",[None])[0]
            if meal and meal not in recipes:
                recipes.append(meal)
        except Exception as e:
            print("Error fetching recipe:", e)
            
    
    return render(request,'includes/dashboard.html',{'recipes':recipes})

@login_required
def new_recipes(request):
    if request.method == 'POST':
        form = NewRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            print("User:", request.user)
            print("User is authenticated:", request.user.is_authenticated)

            return redirect('home')
    else:
        form = NewRecipeForm()
    return render(request, 'new_recipes.html',{'form':form})

@login_required
def profile_view(request):
    user = request.user
    profile = user.createuser
    recipes = NewRecipe.objects.filter(created_by=user)
    
    context = {
        'user':user,
        'profile':profile,
        'recipes':recipes
    }
    return render(request,'includes/profile_detail.html',context)


def delete_recipe(request, id):
    
        recipe = get_object_or_404(NewRecipe, id=id)
        
        if request.method == "POST":
            recipe.delete()
        return render(request,'includes/profile_detail.html',{'recipe':recipe})
            
@login_required
def recipe_list(request):
    user = request.user
    query = request.GET.get('q')
    
    recipes = NewRecipe.objects.filter(created_by=user)
    if query:
        recipes = recipes.filter(Q(title__icontains=query)|Q(ingrediants__icontains=query))
    
    content = {
        'user':user,
        'recipes':recipes,
        'query':query
    }
    
    return render(request, 'recipe_list.html', content)

  