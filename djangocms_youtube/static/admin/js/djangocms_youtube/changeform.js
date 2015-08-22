(function($) {
    $(function() {

        var heightInput = $('input[name="height"]');
        var widthInput = $('input[name="width"]');

        widthInput.keyup(function() {
            var width = $(this).val();
            var height = Math.round((width / 16) * 9);
            heightInput.val(height);
        }).keyup();

        heightInput.keyup(function() {
            var height = $(this).val();
            var width = Math.round((height / 9) * 16);
            widthInput.val(width);
        }).keyup();

        function getYoutubeId(url) {
            var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=)([^#\&\?]*).*/;
            var match = url.match(regExp);
            if (match && match[2].length == 11) {
                return match[2];
            }
            return null;
        }

        $('input[name="video_url"]').on('change', function() {
            var input = $(this),
                url = input.data('gdata'),
                helpText = input.siblings('.help'),
                csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val(),
                videoID = getYoutubeId(input.val());

            input.toggleClass('invalid', !videoID);
            helpText.html('').removeClass('error success');

            if (videoID) {
                var data = {
                    'csrfmiddlewaretoken': csrfmiddlewaretoken,
                    'video_id': videoID
                };

                $.ajax({
                    type: 'POST',
                    url: url,
                    data: data,
                    success: function(response) {
                        $('#id_title').val(response.snippet.title);
                        $('#id_description').val(response.snippet.description);
                        $('#id_video_data').val(JSON.stringify(response, null, 4));
                        helpText.html('Success: Video Located.').addClass('success');
                    },
                    error: function(err) {
                        var response = JSON.parse(err.responseText);
                        if (response.error_type) {
                            helpText.html('An error occurred during validation: ' +
                                response.error_type + ' - ' + response.error_message).addClass('error');
                        } else {
                            helpText.html('We\'re sorry. Something unexpected happened. ' +
                                'Please reload the page and try again.').addClass('error');
                        }
                    }
                });
            }
        })

    });
})(django.jQuery);
