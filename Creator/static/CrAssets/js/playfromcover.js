$('.playlistcover-playicon').click(function(e) {
    e.preventDefault();
    let playlist_id = $(this).data('playlist-id');

    $.ajax({
        type: 'GET',
        url: '/Creator/play_playlist/',
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

    $('.albumcover-playicon').click(function(e) {
        e.preventDefault();
        let album_id = $(this).data('album-id');

        $.ajax({
            type: 'GET',
            url: '/Creator/play_album/',
            data: {
                'album_id': album_id,
            },
            dataType: 'json',
            success: function(data) {
            console.log("Album data received successfully!");
            console.log(data);

            updateAlbumData(data.music_data);
            },

            error: function(error) {
                console.error("Error fetching album data:", error);
            }
        });
        });    