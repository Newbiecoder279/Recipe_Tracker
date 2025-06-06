from django.urls import path
#from . views import home,user_signup, user_login, recipe_detail, user_dashboard,user_logout
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path('', views.home, name='home' ),
    path('signup/',views.user_signup, name='user_signup'),
    path('login/',views.user_login, name='user_login'),
    path('logout/',views.user_logout, name='logout'),
    path('recipe/<int:meal_id>/',views.recipe_detail, name='recipe_detail'),
    path('dashboard/',views.user_dashboard, name='user_dashboard'),
    path('new_recipes/', views.new_recipes, name = 'new_recipes'),
    path('profile/',views.profile_view, name='profile_detail'),
    path('remove/<int:id>/', views.delete_recipe, name='delete_recipe'),
    path('recipe_list',views.recipe_list, name='recipe_list')
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
