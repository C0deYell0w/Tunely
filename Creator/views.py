from django.shortcuts import render,redirect
from Creator.models import*
from AdminApp.models import*
from User.models import*
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from fuzzywuzzy import fuzz
from django.shortcuts import get_object_or_404
import random 
from random import randint
from django.http import JsonResponse
from datetime import date
from django.db.models import Q

# Create your views here.

def CrIndex(request):
        pldata = playlist_data(request)
        notifcdata = notification_data(request)
        messages_to_display = messages.get_messages(request)
        return render(request, "CreatorTemp/CrIndex.html",{'pldata':pldata,
                                                        'messages_to_display':messages_to_display,
                                                        'nfdata': notifcdata,
                                                        })


def playlist_data(request):
    Cr_id = request.session.get('Crid')
    if Cr_id:
        creator = Creators.objects.get(id=Cr_id)
        if creator:
            playlist_data = CrPlaylist.objects.filter(CrId=creator)
            return list(playlist_data)

def notification_data(request):
    Cr_id = request.session.get('Crid')
    if Cr_id:
        creator = Creators.objects.get(id=Cr_id)
        
        if creator:
            notifications_data = Notifications.objects.filter(Crid=creator)
            collab_notifications_data = CollabNotifications.objects.filter(Crid=creator)
            all_notifications_data = list(notifications_data) + list(collab_notifications_data)
            return all_notifications_data
    return []

def delnotification(request,Nid):
    notifc_item = get_object_or_404(Notifications, id=Nid)
    notifc_item.delete()
    return redirect('Creator:CrHome')


def generate_random_color(last_color=None):
    color_palette = [ "#008600","#374ca9","#c9b8ab", "#ff7300", "#ff0059", "#a600ff","#b2702d", "#00ac7e","#dfab01","#7300ff"]
    available_colors = [color for color in color_palette if color != last_color]
    random_color = available_colors[randint(0, len(available_colors) - 1)]
    return random_color

def CrHome(request):
    if 'Crid' in request.session:
        pldata = playlist_data(request)
        notifcdata = notification_data(request)
        langdata = Language.objects.all().order_by('?')[:6]
        gdata = Genre.objects.all().order_by('?')[:6]
        albums_data = Albums.objects.all().order_by('?')[:6]
        music_data = Music.objects.all().order_by('?')[:6]
        current_date = date.today()
        latest_releases = Music.objects.filter(release_date__lt=current_date).order_by('-release_date')[:6]
        last_color = None
        color_list = []
        for item in langdata:
            color = generate_random_color(last_color)
            color_list.append(color)
            last_color = color
        messages_to_display = messages.get_messages(request)
        return render(request, "CreatorTemp/CrHomepage.html", {
                                                            'pldata': pldata,
                                                            'nfdata': notifcdata,
                                                            'Ldata': zip(langdata, color_list),
                                                            'Gdata':gdata,
                                                            'albums_data':albums_data,
                                                            'music_data':music_data,
                                                            'latest_releases':latest_releases,
                                                            'messages_to_display':messages_to_display,
                                                        })
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')



def SignUp(request):
    if request.method == 'POST':
        Fnam = request.POST.get('fnaeme')
        Unam = request.POST.get('usrname')
        Mrole = request.POST.get('musical-role')
        Country = request.POST.get('country')
        Mail = request.POST.get('mail')
        Pass = request.POST.get('pass')
        Creators.objects.create(FullName=Fnam,
                                UsrName=Unam,
                                MusicRole=Mrole,
                                Country=Country,
                                Email=Mail,
                                Password=Pass
                                )
        messages.success(request, 'Your Tunely Creator Account Was Created Sucessfully, Please Login To Continue.')
        return redirect("User:Login.html")
    else:
        return render(request,"CreatorTemp/CreateAccount.html")

def CrProfile(request):
    if 'Crid' in request.session:
        Cr = Creators.objects.get(id=request.session['Crid'])
        AlbumData = Albums.objects.filter(CrId=Cr)
        music = Music.objects.filter(CrId=Cr)[:5]
        Cr=Creators.objects.get(id=request.session['Crid'])
        data = CrPlaylist.objects.filter(CrId=Cr)
        follow_count = Follow.objects.filter(following=Cr).count()
        follow_cr_count = FollowCr.objects.filter(following=Cr).count()
        follower_count = follow_count + follow_cr_count

        creator = get_object_or_404(Creators, id=Cr.id)
        following_creators = Follow.objects.filter(follower=creator)
        followed_creators_details = []
        for follow_relation in following_creators:
            followed_creator = follow_relation.following
            creator_details = {
                'id': followed_creator.id,
                'UsrName': followed_creator.UsrName,
                'Profile_Picture': followed_creator.Profile_Picture.url if followed_creator.Profile_Picture else None,
            }
            followed_creators_details.append(creator_details)

        allmusic = Music.objects.filter(CrId=Cr)
        collabs = Music.objects.filter(Q(collaborator_1=Cr) | Q(collaborator_2=Cr) | Q(collaborator_3=Cr))
        pldata = playlist_data(request)
        notifcdata = notification_data(request)
        messages_to_display = messages.get_messages(request)
        return render(request, "CreatorTemp/CrProfile.html",{'CR':Cr,
                                                            'Mdata':music,
                                                            'Allmusic':allmusic,
                                                            'ALdata':AlbumData,
                                                            'Playlist':data,
                                                            'pldata': pldata,
                                                            'nfdata': notifcdata,
                                                            'collabs': collabs,
                                                            'follower_count': follower_count,
                                                            'messages_to_display': messages_to_display,
                                                            'Following':followed_creators_details,
                                                            })
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def logout(request):
    del request.session["Crid"]
    messages.success(request, 'Logged Out, Successfully')
    return redirect("User:Login") 

def CrEditPage(request,Cid):
    if 'Crid' in request.session:
        Cr=Creators.objects.get(id=Cid)
        pldata = playlist_data(request)
        notifcdata = notification_data(request)
        return render(request, "CreatorTemp/CrEditprofile.html",{'CR':Cr,
                                                                 'pldata': pldata,
                                                                 'nfdata': notifcdata,
                                                                 })
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')


def UpdateProfile(request, Cid):
    if request.method == "POST":
        Unam = request.POST.get("usrname")
        Mrole = request.POST.get("musicrole")
        try:
            banner_img = request.FILES['banner-img']
            fs_banner = FileSystemStorage()
            banner_file = fs_banner.save(banner_img.name, banner_img)
        except MultiValueDictKeyError:
            banner_file = Creators.objects.get(id=Cid).Profile_Banner
        try:
            profile_img = request.FILES['profile-img']
            fs_profile = FileSystemStorage()
            profile_file = fs_profile.save(profile_img.name, profile_img)
        except MultiValueDictKeyError:
            profile_file = Creators.objects.get(id=Cid).Profile_Picture
        Creators.objects.filter(id=Cid).update(UsrName=Unam,
                                               MusicRole=Mrole,
                                               Profile_Banner=banner_file,
                                               Profile_Picture=profile_file
                                               )
        messages.success(request, 'Profile Sucessfully Updated.')
        return redirect("Creator:CrProfile")


def CrchngPass(request):
    if 'Crid' in request.session:
        Creator=Creators.objects.get(id=request.session['Crid'])
        if request.method == "POST":
            Cpass = request.POST.get('currpass')
            NPass = request.POST.get('newpass')
            origpass = Creator.Password
            if Cpass != origpass:
                Error="  incorrect password"
                return render(request,"CreatorTemp/CrchngPass.html",{'ERR':Error})
            else:
                Creators.objects.filter(id=request.session['Crid']).update(Password=NPass)
                del request.session["Crid"]
                messages.success(request, 'Password Changed Sucessfully, Please Login To Continue.')
                return redirect("User:Login")
        pldata = playlist_data(request)
        notifcdata = notification_data(request)
        return render(request, "CreatorTemp/CrchngPass.html",{'pldata': pldata,'nfdata': notifcdata,})
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')


def CrUploads(request):
    if 'Crid' in request.session:
        Genredata = Genre.objects.all()
        Emodata = MusicMood.objects.all()
        Langdata = Language.objects.all()
        session_crid = request.session.get('Crid')
        following_creators = Follow.objects.filter(follower_id=session_crid).values_list('following', flat=True)
        following_creators_data = Creators.objects.filter(id__in=following_creators)    
        Adata = Albums.objects.filter(CrId=session_crid)
        pldata = playlist_data(request)
        notifcdata = notification_data(request)
        messages_to_display = messages.get_messages(request)
        return render(request, "CreatorTemp/CrUploads.html", {
                                                                'Gdata': Genredata,
                                                                'Edata': Emodata,
                                                                'Ldata': Langdata,
                                                                'ALdata': Adata,
                                                                'FollowData': following_creators_data,
                                                                'pldata': pldata,
                                                                'nfdata': notifcdata,
                                                                'messages_to_display':messages_to_display
                                                            })
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')


def MusicUpload(request):
    if request.method == 'POST':
        creator_id = Creators.objects.get(id=request.session.get('Crid'))
        title = request.POST.get('Title')
        audiofile = request.FILES.get('audiofile')
        genre_id = request.POST.get('genreselect')
        album_id = request.POST.get('albumselect')
        lang_id = request.POST.get('langselect')
        date = request.POST.get('Rdate')
        emo_id = request.POST.get('moodselect')
        cover = request.FILES.get('coverimg')
        CrRole = request.POST.get('crrole')
        collab1_id = request.POST.get('collab1')
        collab2_id = request.POST.get('collab2')
        collab3_id = request.POST.get('collab3')
        C1role = request.POST.get('c1role')
        C2role = request.POST.get('c2role')
        C3role = request.POST.get('c3role')

        genre = get_object_or_404(Genre, id=genre_id) if genre_id else None
        lang = get_object_or_404(Language, id=lang_id) if lang_id else None
        album = get_object_or_404(Albums, id=album_id) if album_id else None
        collab1 = get_object_or_404(Creators, id=collab1_id) if collab1_id else None
        collab2 = get_object_or_404(Creators, id=collab2_id) if collab2_id else None
        collab3 = get_object_or_404(Creators, id=collab3_id) if collab3_id else None
        emo = get_object_or_404(MusicMood, id=emo_id) if emo_id else None

        music = Music.objects.create(
            Title=title,
            CrId=creator_id,
            audio_file=audiofile,
            genre=genre,
            Album=album,
            Language=lang,
            Mood=emo,
            release_date=date,
            cover_art=cover,
            Crrole=CrRole,
            collaborator_1=collab1,
            c1role=C1role,
            collaborator_2=collab2,
            c2role=C2role,
            collaborator_3=collab3,
            c3role=C3role
        )

        collaborators = [collab1, collab2, collab3]
        for collaborator in collaborators:
            if collaborator:
                msg = f"{creator_id.UsrName} has added you as a collaborator on their latest music titled '{music.Title}'"
                CollabNotifications.objects.create(Crid=collaborator, FlwCrid=creator_id, Msg=msg)

        messages.success(request, 'Your Music Was Successfully Uploaded.')
        return redirect('Creator:CrProfile')

    return render(request, 'CreatorTemp/CrUploads.html')

def EditMusic(request, Mid):
    if 'Crid' in request.session:
        music = get_object_or_404(Music, id=Mid)
        session_crid = request.session.get('Crid')
        Gdata = Genre.objects.all()
        Emodata = MusicMood.objects.all()
        Langdata = Language.objects.all()
        following_creators = Follow.objects.filter(follower_id=session_crid).values_list('following', flat=True)
        flwCreators = Creators.objects.filter(id__in=following_creators)    
        Adata = Albums.objects.filter(CrId=session_crid)
        if session_crid == music.CrId.id:
            context = {
                'songid':music.id,
                'title': music.Title,
                'crrole':music.Crrole,
                'genre':music.genre,
                'language':music.Language,
                'mood':music.Mood,
                'album':music.Album,
                'cover':music.cover_art.url,
                'collab1':music.collaborator_1 if music.collaborator_1 else None,
                'c1role':music.c1role,
                'collab2':music.collaborator_2 if music.collaborator_2 else None,
                'c2role':music.c2role,  
                'collab3':music.collaborator_3,
                'c3role':music.c3role,
                'Gdata':Gdata, 
                'Edata':Emodata,  
                'Ldata':Langdata,  
                'ALdata':Adata,  
                'FollowData':flwCreators,  
            }
        pldata = playlist_data(request)
        notifcdata = notification_data(request)
        messages_to_display = messages.get_messages(request)
        return render(request, 'CreatorTemp/CrMusicEdit.html', {'context': context,
                                                                'messages_to_display':messages_to_display,
                                                                'pldata': pldata,
                                                                'nfdata': notifcdata,
                                                                })
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def UpdateMusic(request,Mid):
    if request.method == "POST":
        title = request.POST.get("titlename")
        crrole = request.POST.get("crrole")
        genre = request.POST.get("genreselect")
        album = request.POST.get("albumselect")
        language = request.POST.get("langselect")
        mood = request.POST.get("moodselect")
        collab1 = request.POST.get("collab1")
        collab2 = request.POST.get("collab2")
        collab3 = request.POST.get("collab3")
        C1role = request.POST.get("c1role")
        C2role = request.POST.get("c2role")
        C3role = request.POST.get("c3role")
        try:
            cover_img = request.FILES['musiccover']
            fs_banner = FileSystemStorage()
            cover_file = fs_banner.save(cover_img.name, cover_img)
        except MultiValueDictKeyError:
            cover_file = Music.objects.get(id=Mid).cover_art
        Music.objects.filter(id=Mid).update(Title = title,
                                            Crrole = crrole,
                                            genre = genre,
                                            Album = album,
                                            Language = language,
                                            Mood = mood,
                                            cover_art = cover_file,
                                            collaborator_1 = collab1,
                                            collaborator_2 = collab2,
                                            collaborator_3 = collab3,
                                            c1role = C1role,
                                            c2role = C2role,
                                            c3role = C3role,
                                            )
        messages.success(request, 'Changes Sucessfully Applied.')
        return redirect("Creator:EditMusic",Mid)


def delete_music(request, Mid):
    if 'Crid' in request.session:
        music = get_object_or_404(Music, id=Mid)
        creator = Creators.objects.get(id=request.session['Crid'])
        if music.CrId == creator: 
            music.delete()
            messages.success(request, 'Successfully Deleted Music.')
            return redirect('Creator:CrProfile')
        else:
            messages.success(request, 'Access Denied: You do not have permission to delete this music.')
            return redirect('Creator:CrProfile')
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def CrAlbums(request):
    Creator=Creators.objects.get(id=request.session['Crid'])
    if request.method == "POST":
        Aname = request.POST.get('albumname')
        Acover = request.FILES['albumcover']
        Albums.objects.create(Album_Name=Aname,
                              Album_Cover=Acover,
                              CrId=Creator
                              )
        return redirect("Creator:CrProfile")
    return render(request, "CreatorTemp/CrProfile.html")

def AlbumView(request,Aid):
    if 'Crid' in request.session:
        album = get_object_or_404(Albums, id=Aid)
        creator = album.CrId
        session_crid = request.session.get('Crid')
        pldata = playlist_data(request)
        notifcdata = notification_data(request)
        notifcdata = notification_data(request)
        messages_to_display = messages.get_messages(request)
        if session_crid == creator.id:
            Mdata = Music.objects.filter(Album=album)
            return render (request,"CreatorTemp/CrAlbum.html",{'pldata':pldata,'nfdata': notifcdata,'ALdata': album, 'CR': creator,'Mdata':Mdata, 'messages_to_display': messages_to_display})

        return render (request,"CreatorTemp/CrAlbum.html",{'pldata':pldata,'nfdata': notifcdata,'ALdata': album, 'CR': creator,'Mdata':Mdata, 'messages_to_display': messages_to_display})
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def ViewAlbum(request, Aid):
    if 'Crid' in request.session:
        album = get_object_or_404(Albums, id=Aid)
        creator = album.CrId
        session_crid = request.session.get('Crid')
        if session_crid == creator.id:
            return redirect("Creator:AlbumView", Aid=Aid)
        Mdata = Music.objects.filter(Album=album)
        messages_to_display = messages.get_messages(request)
        pldata = playlist_data(request)
        notifcdata = notification_data(request)
        messages_to_display = messages.get_messages(request)
        return render(request, "CreatorTemp/ViewAlbum.html", {'pldata':pldata,'nfdata': notifcdata,'ALdata': album, 'CR': creator,'Mdata':Mdata, 'messages_to_display': messages_to_display})

    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')
    
def UpdateAlbum(request, Aid):
    if request.method == "POST":
        Aname = request.POST.get("albumname")  
        try:
            CoverFile = request.FILES['albumcover']
            fs_banner = FileSystemStorage()
            Acover = fs_banner.save(CoverFile.name, CoverFile)
        except MultiValueDictKeyError:
            Acover = Albums.objects.get(id=Aid).Album_Cover
        Albums.objects.filter(id=Aid).update(Album_Name=Aname,                                 
                                                Album_Cover=Acover,
                                               )
    messages.success(request, 'Album Sucessfully Updated.')
    return redirect("Creator:AlbumView", Aid=Aid)
    
def deleteAlbum(request, Aid):
    if 'Crid' in request.session:
        session_crid = request.session.get('Crid')
        album = get_object_or_404(Albums, id=Aid)
        if session_crid == album.CrId.id:
            album.delete()
            messages.success(request, 'Album Deleted Sucessfully.')
            return redirect('Creator:CrProfile')
        messages.success(request, "Access Denied: You Can't Delete This Album")
        return redirect('Creator:AlbumView',Aid=album.id)
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')


def search(request):
    if 'Crid' in request.session:
        query = request.GET.get('q', '')
        creators_results = Creators.objects.filter(UsrName__icontains=query)
        albums_results = Albums.objects.filter(Album_Name__icontains=query)
        music_results = Music.objects.filter(Title__icontains=query)

        creators_results = sorted(creators_results, key=lambda x: fuzz.partial_ratio(x.UsrName.replace(" ", ""), query.replace(" ", "")), reverse=True)
        albums_results = sorted(albums_results, key=lambda x: fuzz.partial_ratio(x.Album_Name.replace(" ", ""), query.replace(" ", "")), reverse=True)
        music_results = sorted(music_results, key=lambda x: fuzz.partial_ratio(x.Title.replace(" ", ""), query.replace(" ", "")), reverse=True)
        default_profile_image_url = '/static/CrAssets/img/profiledefault.jpg'
        creators_data = [
            {
                'id': creator.id, 
                'FullName': creator.FullName, 
                'UsrName': creator.UsrName,
                'profile':creator.Profile_Picture.url if creator.Profile_Picture and creator.Profile_Picture.url else default_profile_image_url,
            } for creator in creators_results
        ]
        albums_data = [
            {
                'id': album.id, 
                'Album_Name': album.Album_Name, 
                'Creator': album.CrId.UsrName,
                'album_img':album.Album_Cover.url,
            } for album in albums_results
        ]
        music_data = [
            {
                'id': music.id,
                'Title': music.Title,
                'Creator': music.CrId,
                'Collab1': music.collaborator_1 if music.collaborator_1 else None,
                'Collab2': music.collaborator_2 if music.collaborator_2 else None,
                'Collab3': music.collaborator_3 if music.collaborator_3 else None,
                'audio_file': music.audio_file.url,
                'music_cover': music.cover_art.url,
            } for music in music_results
        ]
        creators_and_albums = {}

        for creator in creators_data:
            creator_albums = Albums.objects.filter(CrId=creator['id']).order_by('?')[:5]
            shuffled_albums = list(creator_albums)
            random.shuffle(shuffled_albums)
            albums_for_creator = [{'id': album.id, 'Album_Name': album.Album_Name, 'Album_Image': album.Album_Cover.url} for album in shuffled_albums]
            creators_and_albums[creator['UsrName']] = albums_for_creator
        pldata = playlist_data(request)
        notifcdata = notification_data(request)

        return render(request, 'CreatorTemp/search_results.html', {'creators_data': creators_data,
                                                                    'albums_data': albums_data, 
                                                                    'query': query, 
                                                                    'creators_and_albums': creators_and_albums,
                                                                    'music_data': music_data,
                                                                    'pldata': pldata,
                                                                    'nfdata': notifcdata,
                                                                    })
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')
    
def play_song(request):
    song_id = request.GET.get('song_id')
    default_profile_image_url = '/static/CrAssets/img/profiledefault.jpg'
    try:
        song = Music.objects.get(id=song_id)
        song_data = {
                "MusicId":song.id,
                "name": song.Title,
                "artist": song.CrId.UsrName,
                "img": song.cover_art.url,
                "audio": song.audio_file.url,
                "creatorid": song.CrId.id if song.CrId else None,
                "CrImg": song.CrId.Profile_Picture.url if song.CrId and song.CrId.Profile_Picture else default_profile_image_url,
                "Crrole": song.Crrole if song.Crrole else None,
                "alid":song.Album.id if song.Album else None,
                "alNm":song.Album.Album_Name if song.Album else None,
                "alCvr":song.Album.Album_Cover.url if song.Album else None,
                "rd": song.release_date if song.release_date else None,
                "lang": song.Language.Lang if song.Language else None,
                "genre":song.genre.Genre_Name if song.genre else None,
                "mood":song.Mood.Mood if song.Mood else None,
                "collab1id":song.collaborator_1.id if song.collaborator_1 else None,
                "collab1nm":song.collaborator_1.UsrName if song.collaborator_1 else None,
                "collab1img":song.collaborator_1.Profile_Picture.url if song.collaborator_1 and song.collaborator_1.Profile_Picture else default_profile_image_url,
                "collab1role":song.c1role if song.collaborator_1 else None,
                "collab2id":song.collaborator_2.id if song.collaborator_2 else None,
                "collab2nm":song.collaborator_2.UsrName if song.collaborator_2 else None,
                "collab2img":song.collaborator_2.Profile_Picture.url if song.collaborator_2 and song.collaborator_2.Profile_Picture  else default_profile_image_url,
                "collab2role":song.c2role if song.collaborator_2 else None,
                "collab3id":song.collaborator_3.id if song.collaborator_3 else None,
                "collab3nm":song.collaborator_3.UsrName if song.collaborator_3 else None,
                "collab3img":song.collaborator_3.Profile_Picture.url if song.collaborator_3 and song.collaborator_3.Profile_Picture  else default_profile_image_url,
                "collab3role":song.c3role if song.collaborator_3 else None,
            }
        return JsonResponse(song_data)   
    except Music.DoesNotExist:
        return JsonResponse({'error': 'Song not found'})
    
    
def play_album(request):
    album_id = request.GET.get('album_id')
    default_profile_image_url = '/static/CrAssets/img/profiledefault.jpg'

    try:
        album = Albums.objects.get(id=album_id)
        music_data = Music.objects.filter(Album=album)

        music_list = []

        for song in music_data:
            song_data = {
                "MusicId":song.id,
                "name": song.Title,
                "artist": song.CrId.UsrName,
                "img": song.cover_art.url,
                "audio": song.audio_file.url,
                "creatorid": song.CrId.id if song.CrId else None,
                "CrImg": song.CrId.Profile_Picture.url if song.CrId and song.CrId.Profile_Picture else default_profile_image_url,
                "Crrole": song.Crrole if song.Crrole else None,
                "alid":song.Album.id if song.Album else None,
                "alNm":song.Album.Album_Name if song.Album else None,
                "alCvr":song.Album.Album_Cover.url if song.Album else None,
                "rd": song.release_date if song.release_date else None,
                "lang": song.Language.Lang if song.Language else None,
                "genre":song.genre.Genre_Name if song.genre else None,
                "mood":song.Mood.Mood if song.Mood else None,
                "collab1id":song.collaborator_1.id if song.collaborator_1 else None,
                "collab1nm":song.collaborator_1.UsrName if song.collaborator_1 else None,
                "collab1img":song.collaborator_1.Profile_Picture.url if song.collaborator_1 and song.collaborator_1.Profile_Picture else default_profile_image_url,
                "collab1role":song.c1role if song.collaborator_1 else None,
                "collab2id":song.collaborator_2.id if song.collaborator_2 else None,
                "collab2nm":song.collaborator_2.UsrName if song.collaborator_2 else None,
                "collab2img":song.collaborator_2.Profile_Picture.url if song.collaborator_2 and song.collaborator_2.Profile_Picture  else default_profile_image_url,
                "collab2role":song.c2role if song.collaborator_2 else None,
                "collab3id":song.collaborator_3.id if song.collaborator_3 else None,
                "collab3nm":song.collaborator_3.UsrName if song.collaborator_3 else None,
                "collab3img":song.collaborator_3.Profile_Picture.url if song.collaborator_3 and song.collaborator_3.Profile_Picture  else default_profile_image_url,
                "collab3role":song.c3role if song.collaborator_3 else None,
            }
            music_list.append(song_data)

        response_data = {
            'music_data': music_list,
        }

        return JsonResponse(response_data)

    except Albums.DoesNotExist:
        return JsonResponse({'error': 'Album not found'})

def play_playlist(request):
    playlist_id = request.GET.get('playlist_id')
    default_profile_image_url = '/static/CrAssets/img/profiledefault.jpg'

    try:
        playlist = CrPlaylist.objects.get(id=playlist_id)
        playlist_items = CrPlaylistItem.objects.filter(CrPlid=playlist)
        music_data = Music.objects.filter(id__in=[item.MusicId.id for item in playlist_items])

        music_list = []

        for song in music_data:
            song_data = {
                "MusicId": song.id,
                "name": song.Title,
                "artist": song.CrId.UsrName,
                "img": song.cover_art.url,
                "audio": song.audio_file.url,
                "creatorid": song.CrId.id if song.CrId else None,
                "CrImg": song.CrId.Profile_Picture.url if song.CrId and song.CrId.Profile_Picture else default_profile_image_url,
                "Crrole": song.CrId.MusicRole if song.CrId.MusicRole else None,
                "alid": song.Album.id if song.Album else None,
                "alNm": song.Album.Album_Name if song.Album else None,
                "alCvr": song.Album.Album_Cover.url if song.Album else None,
                "rd": song.release_date,
                "lang": song.Language.Lang if song.Language else None,
                "genre": song.genre.Genre_Name if song.genre else None,
                "mood": song.Mood.Mood,
                "collab1id": song.collaborator_1.id if song.collaborator_1 else None,
                "collab1nm": song.collaborator_1.UsrName if song.collaborator_1 else None,
                "collab1img": song.collaborator_1.Profile_Picture.url if song.collaborator_1 and song.collaborator_1.Profile_Picture else default_profile_image_url,
                "collab1role": song.collaborator_1.MusicRole if song.collaborator_1 else None,
                "collab2id": song.collaborator_2.id if song.collaborator_2 else None,
                "collab2nm": song.collaborator_2.UsrName if song.collaborator_2 else None,
                "collab2img": song.collaborator_2.Profile_Picture.url if song.collaborator_2 and song.collaborator_2.Profile_Picture else default_profile_image_url,
                "collab2role": song.collaborator_2.MusicRole if song.collaborator_2 else None,
            }
            music_list.append(song_data)

        response_data = {
            'music_data': music_list,
        }

        return JsonResponse(response_data)

    except Playlist.DoesNotExist:
        return JsonResponse({'error': 'playlist not found or unauthorized'})
    except PlaylistItem.DoesNotExist:
        return JsonResponse({'error': 'playlistitem not found or unauthorized'})



def ViewProfile(request, Cid):
    if 'Crid' in request.session:
        session_crid = request.session.get('Crid')
        requested_creator = Creators.objects.get(id=Cid)
        if session_crid == requested_creator.id:
            return redirect("Creator:CrProfile")
        topmusic = Music.objects.filter(CrId=Cid)[:5]
        crplaylists = CrPlaylist.objects.filter(CrId=Cid, PlStatus=1)
        AlbumData = Albums.objects.filter(CrId=requested_creator)[:12]
        allmusic = Music.objects.filter(Q(CrId=Cid) | Q(collaborator_1=Cid) | Q(collaborator_2=Cid) | Q(collaborator_3=Cid))
        collabs = Music.objects.filter(Q(collaborator_1=Cid) | Q(collaborator_2=Cid) | Q(collaborator_3=Cid))
        is_following = Follow.objects.filter(follower_id=session_crid, following_id=Cid).exists()
        follow_count = Follow.objects.filter(following=requested_creator).count()
        follow_cr_count = FollowCr.objects.filter(following=requested_creator).count()
        follower_count = follow_count + follow_cr_count
        pldata = playlist_data(request)
        notifcdata = notification_data(request)
        messages_to_display = messages.get_messages(request)
        return render(request, "CreatorTemp/ProfileView.html", {'CR': requested_creator, 
                                                                'ALdata': AlbumData, 
                                                                'is_following': is_following,
                                                                'pldata': pldata,
                                                                'nfdata': notifcdata,
                                                                'Mdata':topmusic,
                                                                'Allmusic':allmusic,
                                                                'Playlist':crplaylists,
                                                                'collabs':collabs,
                                                                'follower_count':follower_count,
                                                                'messages_to_display':messages_to_display,
                                                                })
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')


def Followfn(request, Cid):
    if 'Crid' in request.session:
        session_crid = request.session.get('Crid')
        cr =Creators.objects.get(id=Cid)
        follower = Creators.objects.get(id=session_crid)
        following = Creators.objects.get(id=Cid)
        notification_msg = f"{follower.UsrName} started following you."
        Notifications.objects.create(Crid=following,FlwCrid=follower,Msg=notification_msg)
        Follow.objects.create(follower=follower, following=following)
        messages.success(request, 'Started Following '+cr.UsrName)
        return redirect('Creator:ViewProfile', Cid=Cid)
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def Unfollow(request, Cid):
    if 'Crid' in request.session:
        session_crid = request.session.get('Crid')
        cr =Creators.objects.get(id=Cid)
        follower = get_object_or_404(Creators, id=session_crid)
        following = get_object_or_404(Creators, id=Cid)
        notification_entry = Notifications.objects.filter(Crid=following, FlwCrid=follower).first()
        if notification_entry:
            notification_entry.delete()
        follow_entry = Follow.objects.filter(follower=follower, following=following).first()
        if follow_entry:
            follow_entry.delete()
        messages.success(request, 'Unfollowed '+cr.UsrName)
        return redirect('Creator:ViewProfile', Cid=Cid)
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')



def CreatorPlaylist(request):
    if 'Crid' in request.session:
        if request.method == "POST":
            Pnam = request.POST.get("playlistname")
            Img = request.FILES.get('playlistcover', None)
            creator=Creators.objects.get(id=request.session['Crid'])
            CrPlaylist.objects.create(PlaylistName = Pnam,
                                    Playlist_Cover = Img,
                                    CrId = creator )
        messages.success(request, 'Playlist Successfully Created.')
        return redirect('Creator:AllCrPlaylist')
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def AllCrPlaylist(request):
    if 'Crid' in request.session:
        Cr=Creators.objects.get(id=request.session['Crid'])
        data = CrPlaylist.objects.filter(CrId=Cr)
        pldata = playlist_data(request)
        notifcdata = notification_data(request)
        messages_to_display = messages.get_messages(request)
        
        return render(request,'CreatorTemp/CrAllPlaylist.html',{'Playlist':data,
                                                                'pldata':pldata,
                                                                'nfdata': notifcdata,
                                                                'messages_to_display':messages_to_display,
                                                                })
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def PlaylistView(request, Pid):
    if 'Crid' in request.session:
        session_crid = request.session.get('Crid')
        crplaylist = get_object_or_404(CrPlaylist, id=Pid)
        if session_crid == crplaylist.CrId.id:
            return redirect('Creator:ViewCrPlaylist', Pid=Pid)
        creator = crplaylist.CrId
        playlist_items = CrPlaylistItem.objects.filter(CrPlid=crplaylist)
        songs = Music.objects.filter(id__in=[item.MusicId.id for item in playlist_items])
        pldata = playlist_data(request)
        notifcdata = notification_data(request)
        messages_to_display = messages.get_messages(request)
        return render(request, "CreatorTemp/PlaylistView.html", {
                                                                    'PLdata': crplaylist, 
                                                                    'CR': creator, 
                                                                    'messages_to_display': messages_to_display,
                                                                    'Mdata': songs,
                                                                    'pldata': pldata,
                                                                    'nfdata': notifcdata,
                                                                })
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')
    

def ViewCrPlaylist(request, Pid):
    if 'Crid' in request.session:
        crplaylist = get_object_or_404(CrPlaylist, id=Pid)
        session_crid = request.session.get('Crid')
        if session_crid != crplaylist.CrId.id:
            return redirect('Creator:PlaylistView', Pid=Pid)
        creator = crplaylist.CrId
        playlist_items = CrPlaylistItem.objects.filter(CrPlid=crplaylist)
        songs = Music.objects.filter(id__in=[item.MusicId.id for item in playlist_items])
        pldata = playlist_data(request)
        notifcdata = notification_data(request)
        messages_to_display = messages.get_messages(request)
        return render(request, "CreatorTemp/ViewPlaylist.html", {
                                                                    'PLdata': crplaylist, 
                                                                    'CR': creator, 
                                                                    'messages_to_display': messages_to_display,
                                                                    'Mdata': songs,
                                                                    'pldata': pldata,
                                                                    'nfdata': notifcdata,
                                                                })
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')
    
def deleteCrplaylist(request, Pid):
    if 'Crid' in request.session:
        session_crid = request.session.get('Crid')
        playlist = get_object_or_404(CrPlaylist, id=Pid)
        if session_crid == playlist.CrId.id:
            playlist.delete()
            messages.success(request, 'Item Sucessfully Removed From Playlist.')
            return redirect('Creator:AllCrPlaylist')
        messages.success(request, "Access Denied: You Can't Delete This Album")
        return redirect('Creator:ViewCrPlaylist',Pid=playlist.id)
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def UpdateCrplaylist(request,Pid):
    if 'Crid' in request.session:
        if request.method == "POST":
            Plname = request.POST.get("playlistname")
            try:
                CoverFile = request.FILES['playlistcover']
                fs_banner = FileSystemStorage()
                Pcover = fs_banner.save(CoverFile.name, CoverFile)
            except MultiValueDictKeyError:
                Pcover = CrPlaylist.objects.get(id=Pid).Playlist_Cover if CrPlaylist.objects.get(id=Pid).Playlist_Cover else None
            CrPlaylist.objects.filter(id=Pid).update(
                                                        PlaylistName=Plname,
                                                        Playlist_Cover=Pcover,
                                                    )
            messages.success(request, 'Playlist Successfully Updated.')
            return redirect("Creator:ViewCrPlaylist", Pid=Pid)
        return redirect("Creator:ViewCrPlaylist", Pid=Pid)
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')
    

def get_playlist_status(request, playlist_id):
    if request.method == 'GET':
        playlist = get_object_or_404(CrPlaylist, id=playlist_id)
        return JsonResponse({'status': playlist.PlStatus})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def update_playlist_status(request, playlist_id):
    if request.method == 'GET':
        status = request.GET.get('status')
        new_status = int(status)
        playlist = get_object_or_404(CrPlaylist, id=playlist_id)
        playlist.PlStatus = new_status
        playlist.save()
        if new_status == 0:
            message = ' Updated Playlist Visibility To Private'
        elif new_status == 1:
            message = ' Updated Playlist Visibility To Public'

        return JsonResponse({'status': 'success','message': message})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def AddtoCrPlaylist(request):
    if request.method == 'GET':
        playlist_id = request.GET.get('playlistId')
        music_id = request.GET.get('musicId')
        if 'Crid' not in request.session:
            return JsonResponse({'status': 'error', 'message': 'User not in session'})
        creator_id_from_session = request.session['Crid']
        try:
            crplaylist = CrPlaylist.objects.get(id=playlist_id)
        except crplaylist.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Playlist not found'})
        if creator_id_from_session == crplaylist.CrId.id:
            music = get_object_or_404(Music, id=music_id)
            CrPlaylistItem.objects.create(CrPlid=crplaylist, MusicId=music)
            return JsonResponse({'status': 'success', 'message': 'Added to playlist successfully'})
        return JsonResponse({'status': 'error', 'message': 'User does not own the playlist'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def delete_from_playlist(request, playlist_id, music_id):
    if 'Crid' in request.session:
        playlist = get_object_or_404(CrPlaylist, id=playlist_id)
        music = get_object_or_404(Music, id=music_id)
        playlist_item = get_object_or_404(CrPlaylistItem, CrPlid=playlist, MusicId=music)
        playlist_item.delete()
        messages.success(request, 'Item Sucessfully Removed From Playlist.')
        return redirect('Creator:ViewCrPlaylist',Pid=playlist.id)
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')
    
def songs_by_language(request, Lid):
    if 'Crid' in request.session:
        pldata = playlist_data(request)
        notifcdata = notification_data(request)
        language = Language.objects.get(pk=Lid)
        songs = Music.objects.filter(Language=language)
        context = {
            'language': language,
            'songs': songs,
            'pldata': pldata,
            'nfdata': notifcdata,
        }
        return render(request, 'CreatorTemp/SongsbyLanguage.html', context)
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')
    

def songs_by_genre(request, Gid):
    if 'Crid' in request.session:
        pldata = playlist_data(request)
        notifcdata = notification_data(request)
        try:
            genre = Genre.objects.get(pk=Gid)
            songs = Music.objects.filter(genre=genre)
            context = {
                'genre': genre, 
                'songs': songs, 
                'pldata': pldata, 
                'nfdata': notifcdata
                }
            return render(request, 'CreatorTemp/SongsbyGenre.html', context)
        except Genre.DoesNotExist:
            return render(request, 'CreatorTemp/Homepage.html', {'error_message': 'Genre not found'})
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')
    