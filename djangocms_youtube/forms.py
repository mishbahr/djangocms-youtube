from __future__ import unicode_literals

import re

from django import forms

from .models import Youtube
from .widgets import YoutubeVideoURLWidget


class YoutubeModelForm(forms.ModelForm):

    class Meta:
        model = Youtube
        fields = '__all__'
        widgets = {
            'video_url': YoutubeVideoURLWidget(),
        }

    def clean_video_url(self):
        video_url = self.cleaned_data['video_url']
        pattern = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([\w-]{11})')

        match = re.match(pattern, video_url)
        if not match:
            raise forms.ValidationError('The YouTube video URL is invalid')

        return video_url
