$('.play-edit-music').click(function(e) {
    e.preventDefault();
    let song_id = $(this).closest('.edit-play-icon').data('edit-id');

    $.ajax({
        type: 'GET',
        url: '/Creator/play_song/',
        data: {
        'song_id': song_id,
        },
        dataType: 'json',
        success: function(data) {
        console.log("Data received successfully!");
        console.log(data);
        updateMusicData(data);
        
        
        },
        error: function(error) {
        console.error("Error fetching data:", error);
        }
        
    });
    });