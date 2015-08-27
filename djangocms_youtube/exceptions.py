

class YoutubeAPIError(Exception):
    def __init__(self, status_code, error_type, error_message, *args, **kwargs):
        self.status_code = status_code
        self.error_type = error_type
        self.error_message = error_message

    def __str__(self):
        return '(%s) %s - %s' % (self.status_code, self.error_type, self.error_message)


class YoutubeAPI404(Exception):
    pass
