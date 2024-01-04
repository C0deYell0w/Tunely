$('.album-play-icon').click(function(e) {
    e.preventDefault();
    let playlist_id = $(this).data('playlist-id');

    $.ajax({
        type: 'GET',
        url: '/User/play_playlist/',
        data: {
            'playlist_id': playlist_id,
        },
        dataType: 'json',
        success: function(data) {
        console.log("playlist data received successfully!");
        console.log(data);

       
                updateAlbumData(data.music_data);
        
        },

    error: function (error) {
        console.error("Error fetching playlist data:", error);
    }
    });
    });

