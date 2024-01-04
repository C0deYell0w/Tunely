from django.urls import path
from AdminApp import views
app_name="TunelyAdmin"
urlpatterns = [
    path('Index/',views.Index,name="Index"),
    path('Dash/',views.Dash,name="Dash"),
    
    path('Genre_add/',views.Genre_add,name="Genre_add"),
    path('Language_add/',views.Language_add,name="Language_add"),
    path('Mood_Add/',views.Mood_Add,name="Mood_Add"),

    path('DelGenre/<int:genreid>', views.DelGenre, name="DelGenre"),
    path('DelLang/<int:langid>', views.DelLang, name="DelLang"),
    path('DelMood/<int:Mid>', views.DelMood, name="DelMood"),

    path('logout/', views.logout, name="logout"),


]