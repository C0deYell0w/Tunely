from User.models import *

def playlist_data(request):
    user_id = request.session.get('Usrid')
    if user_id:
        user = FormUser.objects.get(id=user_id)
        if user:
            playlist_data = Playlist.objects.filter(UsrId=user)
            return {'pldata': list(playlist_data)}
    return {}

