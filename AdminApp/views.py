from django.shortcuts import render,redirect
from AdminApp.models import*
from django.contrib import messages


# Create your views here.
def Index(request):
    if 'Admnid' in request.session:
        return render(request,"AdminTemp/index.html")
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def Dash(request):
    return render(request,"AdminTemp/dashboard.html")

def Genre_add(request):
    if 'Admnid' in request.session:
        Genre_Data=Genre.objects.all()
        if request.method=="POST":
            gname = request.POST.get('genre_name')
            gicon = request.FILES['genre_icon']
            Genre.objects.create(Genre_Name=gname,
                                Genre_Icons=gicon)
            return render(request,"AdminTemp/Genre_Add.html",{'Gdata':Genre_Data})
        else:
            return render(request,"AdminTemp/Genre_Add.html",{'Gdata':Genre_Data})
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def DelGenre(request,genreid):
    data=Genre.objects.filter(id=genreid)
    data.delete()
    return redirect("TunelyAdmin:Genre_add")

def Language_add(request):
    if 'Admnid' in request.session:
        ldata = Language.objects.all()
        if request.method=="POST":
            lang = request.POST.get('lang')
            char = request.POST.get('langchar')
            Language.objects.create(Lang=lang,Lang_Char=char)
            return render(request,"AdminTemp/Language_Add.html",{'Langdata':ldata})
        else:
            return render(request,"AdminTemp/Language_Add.html",{'Langdata':ldata})
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def DelLang(request,langid):
    lang=Language.objects.filter(id=langid)
    lang.delete()
    return redirect("TunelyAdmin:Language_add")

def Mood_Add(request):
    if 'Admnid' in request.session:
        Mdata = MusicMood.objects.all()
        if request.method == "POST":
            mood = request.POST.get('mood')
            MusicMood.objects.create(Mood=mood)
            return render(request, "AdminTemp/mood_add.html",{'data':Mdata})
        else:
            return render(request,"AdminTemp/mood_add.html",{'data':Mdata})
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def DelMood(request,Mid):
    mood=MusicMood.objects.filter(id=Mid)
    mood.delete()
    return redirect("TunelyAdmin:Mood_Add")

def logout(request):
    if 'Admnid' in request.session:
        del request.session["Admnid"]
        messages.success(request, 'Logged Out, Successfully')
        return redirect("User:Login")
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')