from django.contrib.sitemaps.views import x_robots_tag
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse

from .video_sitemap import VideoElement


@x_robots_tag
def video_sitemap(request, sitemaps,
                  template_name='djangocms_youtube/sitemap.xml',
                  content_type='application/xml'):

    protocol = request.scheme

    site = get_current_site(request)
    domain = site.domain

    urls = []

    for section, site in sitemaps.items():
        if callable(site):
            site = site()

        for url in site.get_urls():
            location = '{protocol}://{domain}{location}'.format(
                protocol=protocol, domain=domain, location=url.get('location'))
            videos = []
            for plugin in url.get('youtube_plugins', []):
                videos.append(VideoElement(plugin))
            if videos:
                url_info = {
                    'location': location,
                    'videos': videos,
                }
                urls.append(url_info)

    response = TemplateResponse(
        request, template_name, {'urlset': urls}, content_type=content_type)
    return response
