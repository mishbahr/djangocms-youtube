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
